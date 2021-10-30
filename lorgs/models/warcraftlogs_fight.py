# IMPORT STANRD LIBRARIES
from collections import defaultdict
import textwrap
import typing

# IMPORT THIRD PARTY LIBRARIES
import arrow
import mongoengine as me
from lorgs import utils

# IMPORT LOCAL LIBRARIES
from lorgs.lib import mongoengine_arrow
from lorgs.logger import logger
from lorgs.models import warcraftlogs_base
from lorgs.models.raid_boss import RaidBoss
from lorgs.models.warcraftlogs_boss import Boss
from lorgs.models.warcraftlogs_actor import Player
from lorgs.models.wow_spec import WowSpec



def get_composition(players: typing.List[Player]) -> dict:
    """Generate a Composition Dict from a list of Players."""
    players = players or []

    comp: typing.Dict[str, dict] = {
        "roles": defaultdict(int),
        "specs": defaultdict(int),
        "classes": defaultdict(int),
    }

    for player in players:
        comp["roles"][player.spec.role.code] += 1
        comp["classes"][player.spec.wow_class.name_slug] += 1
        comp["specs"][player.spec.full_name_slug] += 1

    comp["roles"] = dict(comp["roles"])
    comp["classes"] = dict(comp["classes"])
    comp["specs"] = dict(comp["specs"])
    return comp


class Fight(warcraftlogs_base.EmbeddedDocument):

    fight_id = me.IntField(primary_key=True)

    start_time: arrow.Arrow = mongoengine_arrow.ArrowDateTimeField()
    duration = me.IntField(default=0)

    # deprecated in favor of "duration".
    end_time_old: arrow.Arrow = mongoengine_arrow.ArrowDateTimeField(db_field="end_time")

    boss_id = me.IntField()
    players: typing.List[Player] = me.ListField(me.EmbeddedDocumentField(Player))
    boss: Boss = me.EmbeddedDocumentField(Boss)

    composition = me.DictField()
    deaths = me.IntField(default=0)
    ilvl = me.FloatField(default=0)
    damage_taken = me.IntField(default=0)

    # boss percentage at the end. (its 0.01 for kills)
    percent = me.FloatField(default=0)
    kill = me.BooleanField(default=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.report = None
        if self.boss:
            self.boss.fight = self
        for player in self.players:
            player.fight = self

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.fight_id}, players={len(self.players)})"

    def summary(self):
        return {
            "report_id": self.report.report_id,
            "fight_id": self.fight_id,
            "percent": self.percent,
            "kill": self.kill,
            "duration": self.duration,
            "boss": {"name": self.boss.raid_boss.full_name_slug} if self.boss else {},
        }

    def as_dict(self, player_ids: typing.List[int] = None) -> dict:

        # Get players
        players = self.players
        if player_ids:
            players = [player for player in players if player.source_id in player_ids]
        players = sorted(players, key=lambda player: (player.spec.role, player.spec, player.total))

        # Return
        return {
            **self.summary(),
            "players": [player.as_dict() for player in players],
            "boss": self.boss.as_dict() if self.boss else {},
        }

    ##########################
    # Attributes

    @property
    def duration_fix(self) -> int:
        # fix for old report, that have no "duration"-field
        if self.duration:
            return self.duration
        duration = self.end_time_old - self.start_time
        return duration.total_seconds()

    @property
    def end_time(self) -> arrow.Arrow:
        return self.start_time.shift(seconds=self.duration_fix)

    @property
    def start_time_rel(self) -> int:
        """Fight start time, relative to its parent report (in milliseconds)."""
        start_time = self.start_time.timestamp() - self.report.start_time.timestamp()
        start_time = start_time * 1000
        return int(start_time)

    @property
    def end_time_rel(self) -> int:
        """fight end time, relative to its parent report (in milliseconds)."""
        end_time = self.end_time.timestamp() -  self.report.start_time.timestamp()
        end_time = end_time * 1000
        return int(end_time)

    @property
    def report_url(self) -> str:
        return f"{self.report.report_url}#fight={self.fight_id}"

    @property
    def raid_boss(self) -> RaidBoss:
        return RaidBoss.get(id=self.boss_id)

    #################################
    # Methods
    #
    def add_player(self, **kwargs) -> Player:
        player = Player(**kwargs)
        player.fight = self
        self.players.append(player)
        return player

    def get_player(self, **kwargs) -> Player:
        """Returns a single Player based on the kwargs."""
        return utils.get(self.players, **kwargs)

    def get_players(self, source_ids=typing.List[int]):
        """Gets multiple players based on source id."""
        return [self.get_player(source_id=source_id) for source_id in source_ids]

    def add_boss(self, boss_id) -> RaidBoss:
        self.boss_id = boss_id
        self.boss = Boss(boss_id=boss_id)
        self.boss.fight = self
        return self.boss

    ############################################################################
    # Query
    #
    @property
    def table_query_args(self) -> str:
        return f"fightIDs: {self.fight_id}, startTime: {self.start_time_rel}, endTime: {self.end_time_rel}"

    ############################################################################
    #   Summary
    #
    def get_summary_query(self):
        """Get the Query to load the fights summary."""
        if self.players:
            return ""

        return textwrap.dedent(f"""\
            reportData
            {{
                report(code: "{self.report.report_id}")
                {{
                    summary: table({self.table_query_args}, dataType: Summary)
                }}
            }}
        """)

    def process_players(self, players_data):
        if not players_data:
            logger.warning("players_data is empty")
            return

        total_damage = players_data.get("damageDone", [])
        total_healing = players_data.get("healingDone", [])

        for composition_data in players_data.get("composition", []):

            spec_data = composition_data.get("specs", [])
            if not spec_data:
                logger.warning("Player has no spec: %s", composition_data.get("name"))
                continue

            spec_data = spec_data[0]
            spec_name = spec_data.get("spec")
            class_name = composition_data.get("type")

            spec = WowSpec.get(name_slug_cap=spec_name, wow_class__name_slug_cap=class_name)
            if not spec:
                logger.warning("Unknown Spec: %s", spec_name)
                continue

            # Get Total Damage or Healing
            spec_role = spec_data.get("role")
            total_data = total_healing if spec_role == "healer" else total_damage
            for data in total_data:
                if data.get("id", -1) == composition_data.get("id"):
                    total = data.get("total", 0) / (self.duration / 1000)
                    break
            else:
                total = 0

            # create and return yield player object
            player = self.add_player()
            player.spec_slug = spec.full_name_slug
            player.source_id = composition_data.get("id")
            player.name = composition_data.get("name")
            player.total = int(total)

        # call this before filtering to always get the full comp
        self.composition = get_composition(self.players)

    def process_overview(self, data):
        """Process the data retured from an Overview-Query."""
        summary_data = data.get("reportData", {}).get("report", {}).get("summary", {}).get("data")
        self.duration = self.duration or (summary_data.get("totalTime") / 1000)
        self.process_players(summary_data)

    async def load_overview(self, force=False):
        """Load this fights Overview.

        Args:
            force(boolean, optional): load even if its already loaded

        """
        if force:
            self.players = []

        if self.players:
            return ""

        query = self.get_summary_query()
        result = await self.client.query(query)
        self.process_overview(result)

    ############################################################################
    #   Load Player:
    #
    def get_player_casts_query(self, player_ids: typing.List[int] = None, cast_limit=1000):
        """Query to fetch the Casts (and buffs) for players in this fight.

        Args:
            player_ids(list[int]): player ids to load
            cast_limit(int, optional): number of casts to load. (default=1000)

        """
        if not self.players:
            raise ValueError("Fight has no players!")

        # filter which players to load
        players = self.get_players(player_ids) if player_ids else self.players
        players_to_load = [player for player in players if not player.casts]
        if not players_to_load:
            return ""

        # construct the query
        player_queries = [player.get_sub_query() for player in players_to_load]
        player_queries = [f"({query})" for query in player_queries]
        player_queries_combined = " or ".join(player_queries)

        return textwrap.dedent(f"""\
            casts: events(
                {self.table_query_args},
                limit: {cast_limit}
                filterExpression: {player_queries_combined}
                )
                {{data}}
            """)

    def process_player_casts(self, query_result):

        report_data = query_result.get("reportData", {}).get("report", {})
        casts_data = report_data.get("casts", {})
        for player in self.players:
            player.process_query_result(casts_data)

    async def load_players(self, player_ids: typing.List[int]):

        query = self.get_player_casts_query(player_ids)
        if not query:
            return  # nothing to load

        result = await self.client.query(query)
        self.process_player_casts(result)

    ############################################################################
    #   Boss
    #

    def get_boss_query(self):
        """Get the Query to load the boss for this fight."""
        if self.boss and self.boss.casts:
            return ""

        if not self.raid_boss:
            return ""

        boss_query = self.raid_boss.get_sub_query()
        return textwrap.dedent(f"""\
            boss: events(
                {self.table_query_args},
                filterExpression: "{boss_query}"
                )
                {{data}}
            """)

    def get_cast_query(self) -> str:
        """Get the Query to load all elements for this Fight."""
        ################
        # get sub queries
        cast_query = self.get_player_casts_query()
        boss_query = self.get_boss_query()
        if not (cast_query or boss_query):
            return ""

        return textwrap.dedent(f"""\
            reportData
            {{
                report(code: "{self.report.report_id}")
                {{
                    {cast_query}
                    {boss_query}
                }}
            }}
        """)

    ################################
    # Processing

    def process_boss(self, boss_data: typing.Dict[str, typing.Any]):
        """Process the Query results for the Boss"""
        if not boss_data:
            return

        if not self.boss:
            self.add_boss(self.boss_id)

        self.boss.process_query_result(boss_data)

    def process_query_result(self, query_result):
        logger.debug("start")
        report_data = query_result.get("report") or {}

        # Boss
        boss_data = report_data.get("boss", {})
        self.process_boss(boss_data)

        # load players
        players_data = report_data.get("players", {}).get("data", {})
        self.process_players(players_data)
        # filter out players with no casts
        self.players = [player for player in self.players if player.casts]

    def process_casts(self, query_result):
        print("process_casts")

    ################################
    # Main
    async def load_casts(self):

        query = self.get_cast_query()
        print("query")
        print(query)
        # result = await self.client.query(query)
        # self.process_casts(result)
