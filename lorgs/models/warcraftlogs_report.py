"""Class and Functions to manage Report-Instances."""

# IMPORT STANRD LIBRARIES
import typing

# IMPORT THIRD PARTY LIBRARIES
import arrow
import mongoengine as me

# IMPORT LOCAL LIBRARIES
from lorgs import utils
from lorgs.lib import mongoengine_arrow
from lorgs.models import warcraftlogs_actor
from lorgs.models import warcraftlogs_base
from lorgs.models.warcraftlogs_actor import Boss
from lorgs.models.warcraftlogs_fight import Fight


class Report(warcraftlogs_base.EmbeddedDocument):
    """Defines a Report read from WarcraftLogs.com and stores in our DB."""

    # 16 digit unique id/code as used on warcraftlogs
    report_id: str = me.StringField(primary_key=True)

    # time the report (!) has started. The first fight might start later
    start_time: arrow.Arrow = mongoengine_arrow.ArrowDateTimeField(default=lambda: arrow.get(0))

    # title of the report
    title: str = me.StringField()

    zone_id: int = me.IntField(default=0)

    # fights in this report keyed by fight_id. (they may or may not be loaded)
    fights: typing.Dict[str, Fight] = me.MapField(me.EmbeddedDocumentField(Fight), default={})

    # players in this report.
    #   Note: not every player might participate in every fight.
    players: typing.Dict[str, warcraftlogs_actor.Player] = me.MapField(me.EmbeddedDocumentField(warcraftlogs_actor.Player), default={})


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # convert list to dict for old DB entries
        if isinstance(self.fights, list):
            self.fights = {fight.fight_id: fight for fight in self.fights}

        for fight in self.fights.values():
            fight.report = self

    def __str__(self):
        return f"<BaseReport({self.report_id}, num_fights={len(self.fights.values())})>"

    ##########################
    # Attributes
    #
    def as_dict(self):
        """Return a Summary/Overview about this report."""
        info = {
            "title": self.title,
            "report_id": self.report_id,
            "date": int(self.start_time.timestamp()),
            "zone_id": self.zone_id,
        }

        # for players and fights we only include essential data
        info["fights"] = {fight.fight_id: fight.summary() for fight in self.fights.values()}
        info["players"] = {player.source_id: player.summary() for player in self.players.values()}
        return info

    ##########################
    # Methods
    #
    def add_fight(self, **fight_data):
        fight = Fight()

        fight.fight_id = fight_data.get("id")
        fight.report = self

        fight.percent = fight_data.get("fightPercentage")
        fight.kill = fight_data.get("kill", True)

        # Fight: Time/Duration
        start_time = fight_data.get("startTime") or 0
        end_time = fight_data.get("endTime") or 0
        fight.start_time = self.start_time.shift(seconds=start_time / 1000)
        fight.duration = (end_time - start_time)

        # store and return
        self.fights[str(fight.fight_id)] = fight
        return fight

    def get_fights(self, *fight_ids: int):
        """Get a multiple fights based of their fight ids."""
        fights = [self.fights.get(str(fight_id)) for fight_id in fight_ids]
        return [f for f in fights if f] # filter out nones

    ##########################
    # Query
    #
    def get_query(self, filters=None):
        """Get the Query to load this Report."""
        # , fight_ids: typing.List[int] = None, fetch_players: bool = False
        master_data_query = """
            masterData
            {
                actors(type: "Player")
                {
                    name
                    id
                    subType
                    icon    # the icon includes the spec name
                }
            }
        """
        return f"""
        reportData
        {{
            report(code: "{self.report_id}")
            {{
                title
                zone {{name id}}
                startTime

                {master_data_query}

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
        """

    def _process_master_data(self, master_data: dict):
        """Create the Players from the passed Report-MasterData"""
        if not master_data:
            return

        # clear out any old instances
        self.players = {}
        for actor_data in master_data.get("actors", []):
            # pets
            if actor_data.get("subType") == "Unknown":
                continue

            player = warcraftlogs_actor.Player()
            player.source_id = actor_data.get("id")
            player.name = actor_data.get("name")

            icon: str = actor_data.get("icon")
            icon_parts = icon.split("-") + [""] # when people swap specs, we only get the class name
            class_name, spec_name, = icon_parts[0:2]
            if not spec_name:
                continue # FIXME: 

            player.class_slug = class_name.lower()
            player.spec_slug = f"{player.class_slug}-{spec_name.lower()}"
            self.players[str(player.source_id)] = player

    def _process_report_fights(self, fights_data):
        """Update the Fights in this report."""
        # clear out any old data
        self.fights = {}

        fights_data = fights_data or []
        for fight_data in fights_data:
            # skip trash fights
            boss_id = fight_data.get("encounterID")
            if not boss_id:
                continue

            # Fight
            fight = self.add_fight(**fight_data)

            # Fight: Boss
            fight.boss = Boss(boss_id=boss_id)
            if fight.boss: # could be a boss unknown to Lorrgs
                fight.boss.fight = fight

    def process_query_result(self, query_result: dict):

        report_data = query_result.get("report", {})

        # Update the Report itself
        self.title = report_data.get("title", "")
        self.start_time = arrow.get(report_data.get("startTime", 0))
        self.zone_id = report_data.get("zone", {}).get("id", -1)

        self._process_master_data(report_data.get("masterData"))
        self._process_report_fights(report_data.get("fights"))

    async def load_fight(self, fight_id: int, player_id=int):
        """Load a single Fight from this Report."""
        fight = self.fights[str(fight_id)]
        if not fight:
            raise ValueError("invalid fight id")

        report_player = utils.get(self.players, source_id=player_id)
        if not report_player:
            raise ValueError("invalid player id")

        # Get or create the player inside the fight
        fight_player = utils.get(fight.players, source_id=player_id)
        if not fight_player:
            fight_player = fight.add_player()
            fight_player.spec_slug = report_player.spec_slug
            fight_player.source_id = report_player.source_id
            fight_player.name = report_player.name

        # LOAD!!!!
        await fight.load()
