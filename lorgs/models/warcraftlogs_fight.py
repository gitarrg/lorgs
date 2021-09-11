# IMPORT STANRD LIBRARIES
import textwrap

# IMPORT THIRD PARTY LIBRARIES
import mongoengine as me

# IMPORT LOCAL LIBRARIES
from lorgs import data
from lorgs import utils
from lorgs.logger import logger
from lorgs.models import warcraftlogs_base
from lorgs.models.encounters import RaidBoss
from lorgs.models.specs import WowClass
from lorgs.models.specs import WowSpec
from lorgs.models.warcraftlogs_actor import Boss
from lorgs.models.warcraftlogs_actor import Player


class Fight(me.EmbeddedDocument, warcraftlogs_base.wclclient_mixin):

    fight_id = me.IntField(primary_key=True)
    start_time = me.IntField(default=0)
    end_time = me.IntField(default=99999999)

    boss_id = me.IntField()

    players = me.ListField(me.EmbeddedDocumentField(Player))
    boss = me.EmbeddedDocumentField(Boss)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.report = None

        if self.boss:
            self.boss.fight = self

        for player in self.players:
            player.fight = self

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.fight_id}, players={len(self.players)})"

    def as_dict(self):
        return {
            "fight_id": self.fight_id,

            "start_time": self.start_time,
            "end_time": self.end_time,
            "duration": self.duration,

            "report_url": self.report_url,
            "num_players": len(self.players),
            "players": [player.as_dict() for player in self.players]
        }

    ##########################
    # Attributes

    @property
    def duration(self):
        return self.end_time - self.start_time

    @property
    def report_url(self):
        return f"{self.report.report_url}#fight={self.fight_id}"

    @property
    def raid_boss(self):
        return RaidBoss.get(id=self.boss_id)

    #################################
    # Methods
    #

    def add_player(self, **kwargs):
        player = Player(**kwargs)
        player.fight = self
        self.players.append(player)
        return player

    def add_boss(self, boss_id):
        self.boss_id = boss_id
        self.boss = Boss(boss_id=boss_id)
        self.boss.fight = self
        return self.boss

    #################################
    # Query
    #

    @property
    def table_query_args(self):
        return f"fightIDs: {self.fight_id}, startTime: {self.start_time}, endTime: {self.end_time}"

    def _build_cast_query(self, filters=None):

        if not filters:
            # we gonna query for all spells
            spell_ids = [spell.spell_id for spell in data.ALL_SPELLS]
            spell_ids = sorted(list(set(spell_ids)))
            spell_ids = ",".join(str(spell_id) for spell_id in spell_ids)
            filters = ["type='cast'", f"ability.id in ({spell_ids})"]

        filters = " and ".join(filters)

        return f"""\
            casts: events(
                {self.table_query_args},
                dataType: Casts,
                filterExpression: "{filters}")
            {{data}}
        """

    def get_query(self, filters=None):

        filters = list(filters or [])

        ################
        #   PLAYERS    #
        ################
        player_query = ""
        cast_query = ""
        if self.players:

            players_to_load = [player for player in self.players if not player.casts]
            if players_to_load:
                cast_query = "casts: "
                # TODO: this probl doesn't work with multiple players
                for player in self.players:
                    cast_query += player.get_sub_query()

        else:
            player_query = f"players: table({self.table_query_args}, dataType: Summary)"
            cast_query = self._build_cast_query(filters)

        ################
        #     BOSS     #
        ################
        boss_query = ""
        if self.boss:
            boss_query = self.boss.get_sub_query()
            boss_query = f"boss: {boss_query}" if boss_query else ""

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
        death_events = players_data.get("deathEvents", [])

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

            player.process_death_events(death_events)

    def process_query_result(self, query_result):

        report_data = query_result.get("report") or {}

        if self.boss:
            boss_casts = report_data.get("boss", {})
            self.boss.process_query_result(boss_casts)

        # load players
        if not self.players: # only if they arn't loaded yet
            players_data = report_data.get("players", {}).get("data", {})
            self.process_fight_players(players_data)

        # load player casts
        if self.players:
            casts_data = report_data.get("casts", {})
            for player in self.players:
                player.process_query_result(casts_data)

        # filter out players with no casts
        self.players = [player for player in self.players if player.casts]
