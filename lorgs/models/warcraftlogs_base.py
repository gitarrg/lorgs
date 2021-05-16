
# IMPORT STANRD LIBRARIES
import textwrap
import abc

# IMPORT THIRD PARTY LIBRARIES
import mongoengine as me

# IMPORT LOCAL LIBRARIES
from lorgs import utils
from lorgs import db
from lorgs.models.specs import WowSpell
from lorgs.client import WarcraftlogsClient
from lorgs.logger import logger
from lorgs.models.specs import WowClass
from lorgs.models.specs import WowSpec
from lorgs.models.specs import WowSpell


class wclclient_mixin:

    @utils.staticproperty
    def client():
        return WarcraftlogsClient.get_instance()

    @abc.abstractmethod
    def get_query(self, filters=None):
        """Get the Query string to fetch all information for this object."""
        return ""

    @classmethod
    async def load_many(cls, objects):
        queries = [obj.get_query() for obj in objects]


class Death:
    """docstring for Cast"""
    def __init__(self, timestamp):
        super().__init__()

        self.timestamp = timestamp
        # self.spell_id = spell_id
        # self.spell = WowSpell.query.get(spell_id)

    def __str__(self):
        time_fmt = utils.format_time(self.timestamp)
        return f"Death(at={time_fmt})"

    def as_dict(self):
        return {
            "timestamp": self.timestamp,
        }


class Cast(me.EmbeddedDocument):
    """docstring for Cast"""

    timestamp = me.IntField()
    spell_id = me.IntField()

    def __str__(self):
        time_fmt = utils.format_time(self.timestamp)
        return f"Cast({self.spell_id}, at={time_fmt})"

    @property
    def spell(self):
        return WowSpell.get(spell_id=self.spell_id)

    def as_dict(self):
        return {
            "timestamp": self.timestamp,
            "spell_id": self.spell_id,
        }


class Player(me.EmbeddedDocument, wclclient_mixin):

    # the actual player
    source_id = me.IntField(primary_key=True) # TODO: rename?
    name = me.StringField(max_length=12) # names can be max 12 chars
    total = me.FloatField()

    # report_id = sa.Column(sa.String(64), sa.ForeignKey("report.report_id"))
    # report = sa.orm.relationship("Report", back_populates="players")

    # fight_id = sa.Column(sa.Integer)
    # fight = sa.orm.relationship("Fight", back_populates="players")

    spec_slug = me.StringField(required=True)

    casts = me.ListField(me.EmbeddedDocumentField(Cast))

    # cast_data = sa.Column(pg.ARRAY(sa.Integer, dimensions=2), default=[])
    # death_data = sa.Column(pg.JSON)

    # __table_args__ = (
    #     sa.ForeignKeyConstraint(
    #         [report_id, fight_id],
    #         ["report_fight.report_id", "report_fight.fight_id"],
    #         ondelete="cascade",
    #     ),
    #     {}
    # )

    # def __init__(self):
    #     super(BasePlayer, self).__init__()
    #     self.spec = None
    #     self.source_id = 0
    #     self.name = ""
    #     self.total = 0
    #     self.cast_data = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fight = None
        self.spec = WowSpec.get(full_name_slug=self.spec_slug)
        # self.boss = encounters.RaidBoss.get(id=self.boss_id)

    def __str__(self):
        return f"Player(id={self.source_id} name={self.name} spec={self.spec})" # casts={len(self.casts)})"

    def as_dict(self):

        return {
            "name": self.name,
            "total": self.total,
            "casts": [cast.as_dict() for cast in self.casts]
        }

    ##########################
    # Attributes
    #
    @property
    def spells_used(self):
        """Only the spells this player has used in this fight."""
        used_spell_ids = set(cast.spell_id for cast in self.casts)
        return [spell for spell in self.spec.spells if spell.spell_id in used_spell_ids]

    @property
    def lifetime(self):
        return self.fight.duration

    #################################
    # Query Helpers
    #
    def process_casts_data(self, casts_data):
        """Process the result of a casts-query to create Cast objects."""
        if not casts_data:
            logger.warning("casts_data is empty")
            return

        for cast_data in casts_data:
            # skip "begincast" events
            if cast_data.get("type") != "cast":
                continue

            # TODO: fetch source_id's?
            if self.source_id >= 0 and cast_data.get("sourceID") != self.source_id:
                continue

            cast = Cast()
            cast.spell_id = cast_data["abilityGameID"]
            cast.timestamp = cast_data["timestamp"] - self.fight.start_time
            self.casts.append(cast)


class Fight(me.EmbeddedDocument, wclclient_mixin):

    meta = {"allow_inheritance": True}

    # __abstract__ = True

    # player_cls = BasePlayer
    # id = sa.Column(sa.Integer(), primary_key=True)
    # report_id = me.StringField()
    fight_id = me.IntField(primary_key=True)
    start_time = me.IntField()
    end_time = me.IntField()

    # report_id = sa.Column(sa.String)
    # report_id = sa.Column(sa.String(64), sa.ForeignKey("report.report_id", ondelete="cascade"), primary_key=True)
    players = me.ListField(me.EmbeddedDocumentField(Player))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.report = None

        for player in self.players:
            player.fight = self

    def __repr__(self):
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

    #################################
    # Methods
    #

    def add_player(self, **kwargs):
        player = Player(**kwargs)
        player.fight = self
        self.players.append(player)
        return player

    #################################
    # Query Helpers
    #
    def get_query(self, filters=None):
        table_query_args = f"fightIDs: {self.fight_id}, startTime: {self.start_time}, endTime: {self.end_time}"

        # spell_ids = ",".join(str(spell.spell_id) for spell in self.spec.spells)
        filters = list(filters or [])

        if not self.players:
            player_query = f"players: table({table_query_args}, dataType: Summary)"
        else:
            player_query = ""

            for player in self.players:
                spell_ids = ",".join(str(spell.spell_id) for spell in player.spec.spells)
                filters += [f"source.name='{player.name}'"]
                filters += [f"ability.id in ({spell_ids})"]

        filter_expr = " and ".join(filters)

        return textwrap.dedent(f"""\
            reportData
            {{
                report(code: "{self.report.report_id}")
                {{
                    {player_query}
                    casts: events({table_query_args}, dataType: Casts, filterExpression: \"{filter_expr}\")
                        {{data}}
                }}
            }}
            """)

    def load_fight_players(self, players_data):
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
            player = Player()
            player.fight = self
            player.spec = spec
            player.spec_slug = spec.full_name_slug
            player.source_id = composition_data.get("id")
            player.name = composition_data.get("name")
            player.total = total
            self.players.append(player)

    def process_query_result(self, query_result):

        report_data = query_result.get("report") or {}

        # load players
        players_data = report_data.get("players", {}).get("data", {})
        if not self.players: # only if they arn't loaded yet
            self.load_fight_players(players_data)

        # load player casts
        casts_data = report_data.get("casts", {}).get("data", [])
        for player in self.players:
            player.process_casts_data(casts_data)

        # filter out players with no casts
        self.players = [player for player in self.players if player.casts]

    @classmethod
    async def load_many(cls, fights, filters=None, chunk_size=0):
        """Load multiple fights at once.

        Args:
            fights(list[Fights]): the fights to load
            filters(list[str], optional): extra argument used to filter fight casts
            chunks_size[int, optional]: load in chunks of this size.

        """
        for fights_chunk in utils.chunks(fights, chunk_size):

            queries = [fight.get_query(filters or []) for fight in fights_chunk]
            data = await cls.client.multiquery(queries)

            for fight, fight_data in zip(fights_chunk, data):
                fight.process_query_result(fight_data)


class Report(me.EmbeddedDocument, wclclient_mixin):

    report_id = me.StringField(primary_key=True)
    start_time = me.IntField(default=0)
    fights = me.ListField(me.EmbeddedDocumentField(Fight))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for fight in self.fights:
            fight.report = self

    def __str__(self):
        return f"<BaseReport({self.report_id}, num_fights={len(self.fights)})>"

    def as_dict(self):
        return {
            "code": self.report_id,
            "start_time": self.start_time,
            "num_fights": len(self.fights),
            "fights": [fight.as_dict() for fight in self.fights]
        }

    ##########################
    # Attributes
    #
    @property
    def players(self):
        return utils.flatten(fight.players for fight in self.fights)

    @property
    def report_url(self):
        return f"https://warcraftlogs.com/reports/{self.report_id}/"

    ##########################
    # Methods
    #

    def add_fight(self, **kwargs):
        fight = Fight(**kwargs)
        fight.report = self
        self.fights.append(fight)
        return fight
