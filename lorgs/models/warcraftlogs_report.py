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

    # list of fights in this report. (they may or may not be loaded)
    fights: typing.List[Fight] = me.ListField(me.EmbeddedDocumentField(Fight))

    # players in this report.
    #   Note: not every player might participate in every fight.
    players: typing.List[warcraftlogs_actor.Player] = me.EmbeddedDocumentListField(warcraftlogs_actor.Player, default=[], db_field="players")


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fight in self.fights:
            fight.report = self

    def __str__(self):
        return f"<BaseReport({self.report_id}, num_fights={len(self.fights)})>"

    ##########################
    # Attributes
    #
    def as_dict(self):
        """Return a Summary/Overview about this report."""
        info = {
            "title": self.title,
            "report_id": self.report_id,
            "date": int(self.start_time.timestamp()),
        }

        # for players and fights we only include essential data
        info["fights"] = [{
            "fight_id": fight.fight_id,
            "boss_slug": fight.boss.raid_boss.full_name_slug,
            "percent": fight.percent,
            "duration": fight.duration,
            } for fight in self.fights]

        info["players"] = [{
            "name": player.name,
            "source_id": player.source_id,
            "spec": player.spec_slug,
            "role": player.spec.role.code,
            } for player in self.players]

        return info

    ##########################
    # Methods
    #
    def add_fight(self, **kwargs):
        fight = Fight(**kwargs)
        fight.report = self
        self.fights.append(fight)
        return fight

    def get_fight(self, **kwargs) -> Fight:
        """Returns a single Fight based on the kwargs."""
        return utils.get(self.fights, **kwargs)

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
        self.players = []
        for actor_data in master_data.get("actors", []):
            # pets
            if actor_data.get("subType") == "Unknown":
                continue

            player = warcraftlogs_actor.Player()
            player.source_id = actor_data.get("id")
            player.name = actor_data.get("name")

            icon: str = actor_data.get("icon")
            class_name, spec_name = icon.split("-")
            player.spec_slug = f"{class_name.lower()}-{spec_name.lower()}"
            self.players.append(player)

    def _process_report_fights(self, fights_data):
        """Update the Fights in this report."""
        # clear out any old data
        self.fights = []

        fights_data = fights_data or []
        for fight_data in fights_data:
            # skip trash fights
            boss_id = fight_data.get("encounterID")
            if not boss_id:
                continue

            # Fight
            fight = self.add_fight()
            fight.fight_id = fight_data.get("id")
            fight.percent = fight_data.get("fightPercentage")

            # Fight: Boss
            fight.boss = Boss(boss_id=boss_id)
            if fight.boss: # could be a boss unknown to Lorrgs
                fight.boss.fight = fight

            # Fight: Time/Duration
            start_time = fight_data.get("startTime") or 0
            end_time = fight_data.get("endTime") or 0
            fight.start_time = self.start_time.shift(seconds=start_time / 1000)
            fight.duration = (end_time - start_time)

    def process_query_result(self, query_result: dict):

        report_data = query_result.get("report", {})

        # Update the Report itself
        self.title = report_data.get("title", "")
        self.start_time = arrow.get(report_data.get("startTime", 0))
        self._process_master_data(report_data.get("masterData"))
        self._process_report_fights(report_data.get("fights"))

    async def load_fight(self, fight_id: int, player_id=int):
        """Load a single Fight from this Report."""
        fight = self.get_fight(fight_id=fight_id)
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
