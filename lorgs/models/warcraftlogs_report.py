"""Class and Functions to manage Report-Instances."""

# IMPORT STANRD LIBRARIES
import typing
import textwrap
import asyncio

# IMPORT THIRD PARTY LIBRARIES
import arrow
import mongoengine as me

# IMPORT LOCAL LIBRARIES
from lorgs import utils
from lorgs.clients import wcl
from lorgs.lib import mongoengine_arrow
from lorgs.logger import logger
from lorgs.models import warcraftlogs_base
from lorgs.models.warcraftlogs_boss import Boss
from lorgs.models.warcraftlogs_fight import Fight
from lorgs.models.warcraftlogs_player import Player


class Report(warcraftlogs_base.EmbeddedDocument):
    """Defines a Report read from WarcraftLogs.com and stores in our DB."""

    # 16 digit unique id/code as used on warcraftlogs
    report_id: str = me.StringField(primary_key=True)

    # time the report (!) has started. The first fight might start later
    start_time: arrow.Arrow = mongoengine_arrow.ArrowDateTimeField(default=lambda: arrow.get(0))

    # title of the report
    title: str = me.StringField()

    zone_id: int = me.IntField(default=0)

    # The guild that the report belongs to. None if it was a logged as a personal report
    guild: str = me.StringField(default="")

    # The user that uploaded the report.
    owner: str = me.StringField(default="")

    # fights in this report keyed by fight_id. (they may or may not be loaded)
    fights: dict[str, Fight] = me.MapField(me.EmbeddedDocumentField(Fight), default={})

    # players in this report.
    #   Note: not every player might participate in every fight.
    players: dict[str, Player] = me.MapField(me.EmbeddedDocumentField(Player), default={})

    def __init__(self, *args: typing.Any, **kwargs: typing.Any):
        super().__init__(*args, **kwargs)
        for fight in self.fights.values():
            fight.report = self

    def __str__(self):
        return f"<BaseReport({self.report_id}, num_fights={len(self.fights)})>"

    ##########################
    # Attributes
    #
    def as_dict(self) -> dict[str, typing.Any]:
        """Return a Summary/Overview about this report."""
        info = {
            "title": self.title,
            "report_id": self.report_id,
            "date": int(self.start_time.timestamp()),
            "zone_id": self.zone_id,
            "guild": self.guild,
            "owner": self.owner,
        }

        # for players and fights we only include essential data
        info["fights"] = {fight.fight_id: fight.summary() for fight in self.fights.values()}
        info["players"] = {player.source_id: player.summary() for player in self.players.values()}
        return info

    ##########################
    # Methods
    #
    def add_fight(self, fight_data: wcl.ReportFight):
        """Add a new Fight to this Report."""
        # skip trash fights
        if not fight_data.encounterID:
            return

        fight = Fight()
        fight.fight_id = fight_data.id
        fight.report = self

        fight.percent = fight_data.fightPercentage
        fight.kill = fight_data.kill

        # Fight: Time/Duration
        start_time = fight_data.startTime / 1000
        end_time = fight_data.endTime / 1000
        fight.start_time = self.start_time.shift(seconds=start_time)
        fight.duration = int((end_time - start_time) * 1000)

        # Fight: Boss
        fight.boss = Boss(boss_id=fight_data.encounterID)
        if fight.boss: # could be a boss unknown to Lorrgs
            fight.boss.fight = fight

        # store and return
        self.fights[str(fight.fight_id)] = fight
        return fight

    def get_fight(self, fight_id: int):
        """Get a single fight from this Report."""
        return self.fights.get(str(fight_id))

    def get_fights(self, *fight_ids: int):
        """Get a multiple fights based of their fight ids."""
        fights = [self.get_fight(fight_id) for fight_id in fight_ids]
        return [f for f in fights if f] # filter out nones

    def add_player(self, actor_data: wcl.ReportActor):

        if actor_data.type != "Player":
            return

        # guess spec from the icon
        # WCL gives us an icon matching the spec, IF a player
        # played the same spec in all fights inside a report.
        # Otherwise it only includes a class-name.
        icon_name = actor_data.icon
        spec_slug = icon_name.lower() if "-" in icon_name else ""

        # create the new player
        player = Player(
            source_id=actor_data.id,
            name=actor_data.name,
            class_slug = actor_data.subType.lower(),
            spec_slug=spec_slug,
        )
        if player.spec == None:
            logger.debug("Skipping unknown Player: %s", player)
            return

        # add to to the report
        self.players[str(player.source_id)] = player

    ############################################################################
    # Query
    #
    def get_query(self):
        """Get the Query to load this Reports Overview."""
        return textwrap.dedent(f"""
        reportData
        {{
            report(code: "{self.report_id}")
            {{
                title
                zone {{name id}}
                startTime

                owner {{ name }}

                guild {{
                    name
                    server {{ name }}
                }}

                masterData
                {{
                    actors(type: "Player")
                    {{
                        name
                        id
                        subType
                        icon    # the icon includes the spec name
                    }}
                }}

                fights
                {{
                    id
                    encounterID
                    startTime
                    endTime
                    fightPercentage
                    kill
                }}
            }}
        }}
        """)

    def process_master_data(self, master_data: wcl.ReportMasterData):
        """Create the Players from the passed Report-MasterData"""
        # clear out any old instances
        self.players = {}

        for actor_data in master_data.actors:
            self.add_player(actor_data)

    def process_report_fights(self, fights: list[wcl.ReportFight]):
        """Update the Fights in this report."""
        # clear out any old data
        self.fights = {}
        for fight in fights:
            self.add_fight(fight)

    def process_query_result(self, **query_result: typing.Any):
        report_data = wcl.ReportData(**query_result)
        report = report_data.report

        # Update the Report itself
        self.title = report.title
        self.start_time = arrow.get(report.startTime)
        self.zone_id = report.zone.id
        self.owner = report.owner.name

        guild = report.guild
        self.guild = guild.name if guild else ""

        if report.masterData:
            self.process_master_data(report.masterData)
        self.process_report_fights(report.fights)

    async def load_summary(self, raise_errors=False) -> None:
        await self.load(raise_errors=raise_errors)

    async def load_fight(self, fight_id: int, player_ids: list[int]):
        """Load a single Fight from this Report."""
        fight = self.fights[str(fight_id)]
        if not fight:
            raise ValueError("invalid fight id")

        await fight.load_players(player_ids=player_ids)

    async def load_fights(self, fight_ids: typing.List[int], player_ids: typing.List[int]):

        if not self.fights:
            await self.load_summary()

        # queue all tasks at once.
        # the client will make sure its throttled accordingly 
        tasks = [self.load_fight(fight_id=fight_id, player_ids=player_ids) for fight_id in fight_ids]
        await asyncio.gather(*tasks)
