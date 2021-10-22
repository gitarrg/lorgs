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
from lorgs.models.warcraftlogs_actor import Boss
from lorgs.models.warcraftlogs_actor import Player
from lorgs.models.wow_spec import WowSpec
from lorgs.models.wow_spell import WowSpell


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


class Fight(me.EmbeddedDocument, warcraftlogs_base.wclclient_mixin):

    fight_id = me.IntField(primary_key=True)

    start_time: arrow.Arrow = mongoengine_arrow.ArrowDateTimeField()
    duration = me.IntField(default=0)

    # deprecated in favor of "duration".
    end_time_old: arrow.Arrow = mongoengine_arrow.ArrowDateTimeField(db_field="end_time")

    boss_id = me.IntField()
    players = me.ListField(me.EmbeddedDocumentField(Player))
    boss = me.EmbeddedDocumentField(Boss)

    composition = me.DictField()
    deaths = me.IntField(default=0)
    ilvl = me.FloatField(default=0)
    damage_taken = me.IntField(default=0)

    # boss percentage at the end. (its 0.01 for kills)
    percent = me.FloatField(default=0)
    kill = me.BooleanField(default=True)

    meta = {
        "strict": False # ignore non existing properties
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.report = None

        if self.boss:
            self.boss.fight = self

        for player in self.players:
            player.fight = self

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.fight_id}, players={len(self.players)})"

    def as_dict(self) -> dict:
        players = sorted(self.players, key=lambda player: (player.spec.role, player.spec, player.total))

        return {
            "fight_id": self.fight_id,
            "report_id": self.report.report_id,
            "duration": self.duration_fix,
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

    def add_boss(self, boss_id) -> RaidBoss:
        self.boss_id = boss_id
        self.boss = Boss(boss_id=boss_id)
        self.boss.fight = self
        return self.boss

    #################################
    # Query
    #

    @property
    def table_query_args(self) -> str:
        return f"fightIDs: {self.fight_id}, startTime: {self.start_time_rel}, endTime: {self.end_time_rel}"

    def _build_cast_query(self, filters: typing.List[str] = None, cast_limit=1000) -> str:
        """
        Args:
            cast_limit (int): maximum number of casts to query.
            (not sure if we need to loop trough pages..)

        """
        if not filters:
            # we gonna query for all spells
            spell_ids = WowSpell.spell_ids_str(WowSpell.all)
            filters = ["type='cast'", f"ability.id in ({spell_ids})"]

        filters = " and ".join(filters) # type: ignore

        return f"""\
            casts: events(
                limit: {cast_limit}
                {self.table_query_args},
                dataType: Casts,
                filterExpression: "{filters}")
            {{data}}
        """

    def get_query(self, filters: typing.List[str] = None) -> str:

        filters = list(filters or [])

        ################
        #   PLAYERS    #
        ################
        player_query = ""
        cast_query = ""
        if self.players:

            players_to_load = [player for player in self.players if not player.casts]
            if players_to_load:

                # combine the filters
                player_filters = [player.get_sub_query() for player in players_to_load]
                player_filters = [f"({f})" for f in player_filters] # wrap each in ()
                player_filters_combined = " or ".join(player_filters)

                # construct the query
                cast_query = f"""\
                    casts: events(
                        {self.table_query_args}
                        filterExpression: \"{player_filters_combined}\"
                    )
                    {{data}}
                """

        else:
            player_query = f"players: table({self.table_query_args}, dataType: Summary)"
            cast_query = self._build_cast_query(filters)

        ################
        #     BOSS     #
        ################
        boss_query = ""
        if self.boss and not self.boss.casts:
            boss_query = self.boss.get_sub_query()
            boss_query = f"boss: {boss_query}" if boss_query else ""

        if not (player_query or cast_query or boss_query):
            return ""

        return textwrap.dedent(f"""\
            reportData
            {{
                report(code: "{self.report.report_id}")
                {{
                    {player_query}
                    {cast_query}
                    {boss_query}
                }}
            }}
        """)

    def process_fight_players(self, players_data):
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
            player.total = total

    def process_query_result(self, query_result):
        logger.debug("start")
        report_data = query_result.get("report") or {}

        if self.boss:
            boss_casts = report_data.get("boss", {})
            self.boss.process_query_result(boss_casts)

        # load players
        if not self.players: # only if they arn't loaded yet
            logger.debug("create players")
            players_data = report_data.get("players", {}).get("data", {})
            self.process_fight_players(players_data)

            # call this before filtering to always get the full comp
            self.composition = get_composition(self.players)

        # load player casts
        if self.players:
            logger.debug("create player casts")
            casts_data = report_data.get("casts", {})
            logger.debug("num casts: %d", len(casts_data.get("data", [])))

            for player in self.players:
                player.process_query_result(casts_data)

        # filter out players with no casts
        self.players = [player for player in self.players if player.casts]
