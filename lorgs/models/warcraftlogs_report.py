"""Models for Warcraftlog-Reports/Fights/Actors."""

# pylint: disable=too-few-public-methods

# IMPORT STANRD LIBRARIES
# import datetime
# import arrow
import textwrap

# IMPORT THIRD PARTY LIBRARIES
# import sqlalchemy
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql as pg
# from sqlalchemy import sa.Column, sa.ForeignKey
# from sqlalchemy import sa.Integer, String, Bigsa.Integer, sa.Unicode, Float
# from sqlalchemy.orm import sa.orm.relationship

# IMPORT LOCAL LIBRARIES
from lorgs import db
from lorgs import utils
# from lorgs.cache import Cache
from lorgs.client import WarcraftlogsClient
from lorgs.logger import logger
# from lorgs.models import base
from lorgs.models.encounters import RaidBoss
# from lorgs.models.encounters import RaidZone
from lorgs.models.specs import WowClass
from lorgs.models.specs import WowSpec
from lorgs.models.specs import WowSpell
from lorgs.models import warcraftlogs_base

# raise ValueError("Dont import me")


class Report(db.Base):
    """docstring for Fight"""

    __tablename__ = "report"

    # attributes
    report_id = sa.Column(sa.String(64), primary_key=True)
    start_time = sa.Column(sa.BigInteger(), default=0)
    title = sa.Column(sa.Unicode(128))

    # sa.orm.relationships
    zone = sa.orm.relationship("RaidZone")
    zone_id = sa.Column(sa.Integer, sa.ForeignKey("raid_zone.id"))

    fights = sa.orm.relationship(
        "Fight",
        back_populates="report",
        cascade="all,delete,delete-orphan",
        lazy="joined"
    )

    players = sa.orm.relationship(
        "Player",
        back_populates="report",
        cascade="all,delete,delete-orphan",
        lazy="dynamic"
    )

    def __repr__(self):
        return f"<Report({self.report_id})>"

    def as_dict(self):
        return {
            "report_id": self.report_id,
            "title": self.title,
            "start_time": self.start_time,
            "zone": self.zone.as_dict() if self.zone else {},
            "fights": [fight.as_dict() for fight in self.fights]
        }

    @property
    def report_url(self):
        return f"https://www.warcraftlogs.com/reports/{self.report_id}"

    ############################################
    #
    #       QUERY
    #
    ############################################

    @property
    def client(self):
        return WarcraftlogsClient.get_instance()

    async def load_report_info(self, fight_ids=None):
        """Fetch all fights in this report.

        Args:
            fight_ids(list[int], optional): list of fights to load.
                loads all fights, if not specified.

        """
        query = f"""
        reportData
        {{
            report(code: "{self.report_id}")
            {{
                title
                zone {{name id}}
                startTime

                # masterData
                # {{
                #     actors(type: "Player")
                #     {{
                #         name
                #         id
                #     }}
                # }}

                fights(fightIDs: {fight_ids or []})
                {{
                    id
                    encounterID
                    startTime
                    endTime
                    fightPercentage
                    # kill
                }}
            }}
        }}
        """
        data = await self.client.query(query)
        report_data = data.get("reportData", {}).get("report", {})

        # Update the Report itself
        self.title = report_data.get("title", "")
        self.start_time = report_data.get("startTime", 0)
        self.zone_id = report_data.get("zone", {}).get("id")

        # Update the Fights in this report
        for fight_data in report_data.get("fights", []):

            boss_id = fight_data.get("encounterID")
            if not boss_id:
                continue

            # Get the fight
            fight = Fight()
            fight.fight_id = fight_data.get("id")
            fight.start_time = fight_data.get("startTime", 0)
            fight.end_time = fight_data.get("endTime", 0)
            fight.boss_id = boss_id # RaidBoss.query.get(boss_id)
            fight.percent = fight_data.get("fightPercentage")
            self.fights.append(fight)

    async def load(self):
        if not self.fights:
            logger.info(f"{self} | load info")
            await self.load_report_info()

        # TODO: load in batch
        for fight in self.fights:
            await fight.load()


class Fight(db.Base):
    """Basically a pull."""

    __tablename__ = "report_fight"

    # attributes
    fight_id = sa.Column(sa.Integer, primary_key=True)
    start_time = sa.Column(sa.BigInteger)
    end_time = sa.Column(sa.BigInteger)
    percent = sa.Column(sa.Float, default=0)

    # relationships
    report_id = sa.Column(sa.String(64), sa.ForeignKey("report.report_id", ondelete="cascade"), primary_key=True)
    report = sa.orm.relationship("Report", back_populates="fights")

    boss_id = sa.Column(sa.Integer(), sa.ForeignKey("raid_boss.id"))
    boss = sa.orm.relationship("RaidBoss")

    # children
    players = sa.orm.relationship(
        "Player",
        back_populates="fight",
        cascade="all,delete,delete-orphan",
    )

    __mapper_args__ = {
        "order_by" : fight_id
    }

    def __repr__(self):
        return f"Fight({self.report_id}, id={self.fight_id}, players={len(self.players)})"

    def as_dict(self, fights=True):
        return {
            "fight_id": self.fight_id,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "percent": self.percent,
            "boss": self.boss.as_dict() if self.boss else {},
            # "players": [player.as_dict() for player in self.players],
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
    def percent_color(self):
        if self.percent < 3:
            return "astounding"
        if self.percent < 10:
            return "legendary"
        if self.percent < 25:
            return "epic"
        if self.percent < 50:
            return "rare"
        if self.percent < 75:
            return "uncommon"
        return "common"

    ############################################
    #
    #       QUERY
    #
    ############################################

    @property
    def client(self):
        return WarcraftlogsClient.get_instance()

    def get_fight_data_query(self, spells=None):
        """Construct the Query to fetch all info in a Fight.

        Args:
            fight(<Fight>): the fight we want to fetch
            spells[list(Spell)]: the spells we want to fetch (queries all spells if None)

        Returns:
            str: the constructed query string

        """
        table_query_args = f"fightIDs: {self.fight_id}, startTime: {self.start_time}, endTime: {self.end_time}"

        player_query = f"players: table({table_query_args}, dataType: Summary)"

        spells = spells or WowSpell.query.all()
        spell_ids = sorted(spell.spell_id for spell in spells)
        spell_ids = ",".join(str(i) for i in spell_ids)
        casts_filter = f"ability.id in ({spell_ids})"
        casts_query = f"casts: events({table_query_args}, dataType: Casts, filterExpression: \"{casts_filter}\") {{data}}"

        # logger.debug("player_query: %s", player_query)
        # logger.debug("casts_filter: %s", casts_filter)

        return textwrap.dedent(f"""\
        reportData {{
            report(code: "{self.report.report_id}") {{
                {player_query}
                {casts_query}
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
            player.spec = spec
            player.source_id = composition_data.get("id")
            player.name = composition_data.get("name")
            player.total = total
            self.players.append(player)

    def procress_query_data(self, query_data):

        report_data = query_data.get("report") or {}

        # process players
        players_data = report_data.get("players", {}).get("data", {})
        if not self.players: # only if they arn't loaded yet
            self.load_fight_players(players_data)

        # process casts
        casts_data = report_data.get("casts", {}).get("data", [])
        for player in self.players:
            player.load_player_casts(casts_data)

            player.process_extra_data(players_data)

    async def load(self):
        query = self.get_fight_data_query()
        data = await self.client.query(query)

        data = data.get("reportData", {})
        self.procress_query_data(data)


class Player(db.Base):
    """a player in a given fight.

    TODO:
        rename to actor?

    """
    __tablename__ = "report_player"

    id = sa.Column(sa.Integer(), primary_key=True)

    # the actual player
    source_id = sa.Column(sa.Integer())  # TODO: rename?
    name = sa.Column(sa.Unicode(12)) # names can be max 12 chars
    total = sa.Column(sa.Integer)

    report_id = sa.Column(sa.String(64), sa.ForeignKey("report.report_id"))
    report = sa.orm.relationship("Report", back_populates="players")

    fight_id = sa.Column(sa.Integer)
    fight = sa.orm.relationship("Fight", back_populates="players")

    cast_data = sa.Column(pg.ARRAY(sa.Integer, dimensions=2), default=[])
    death_data = sa.Column(pg.JSON)

    spec = sa.orm.relationship("WowSpec")
    spec_id = sa.Column(sa.Integer, sa.ForeignKey("wow_spec.id"))

    __table_args__ = (
        sa.ForeignKeyConstraint(
            [report_id, fight_id],
            ["report_fight.report_id", "report_fight.fight_id"],
            ondelete="cascade",
        ),
        {}
    )

    def __repr__(self):
        return f"Player(id={self.source_id} name={self.name} spec={self.spec})" # casts={len(self.casts)})"

    def as_dict(self):
        return {
            "source_id": self.source_id,
            "name": self.name,
            "total": self.total,
            "spec": self.spec.full_name_slug if self.spec else "",
            "casts": [cast.as_dict() for cast in self.casts]
        }

    @property
    def casts(self):
        cast_data = self.cast_data or []
        return [warcraftlogs_base.Cast(timestamp, spell_id) for timestamp, spell_id in cast_data]

    @property
    def used_spells(self):
        # spec_spells = self.spec.spells
        used_spell_ids = [cast.spell_id for cast in self.casts]
        return [spell for spell in self.spec.spells if spell.spell_id in used_spell_ids]

    @property
    def lifetime(self):
        if self.death_data:
            return self.death_data[-1].get("deathTime", 0)

        return self.fight.duration


    ############################################
    #
    #       QUERY
    #
    ############################################

    def load_player_casts(self, casts_data):
        """Process the result of a casts-query to create Cast objects."""
        if not casts_data:
            logger.warning("casts_data is empty")
            return

        self.cast_data = self.cast_data or []

        for cast_data in casts_data:
            if cast_data.get("sourceID") != self.source_id:
                continue

            # skip "begincast" events
            if cast_data.get("type") != "cast":
                continue

            spell_id = cast_data["abilityGameID"]
            timestamp = cast_data["timestamp"] - self.fight.start_time
            self.cast_data.append([timestamp, spell_id])

    def process_extra_data(self, players_data):

        # Deaths
        self.death_data = self.death_data or []
        for death_event in players_data.get("deathEvents", []):

            if death_event.get("id") != self.source_id:
                continue

            death_data = {}
            death_data["deathTime"] = death_event.get("deathTime")
            death_data["ability"] = death_event.get("ability", {})

            # Fall Damage
            if death_data["ability"].get("guid") == 3:
                death_data["ability"] = {}

            self.death_data.append(death_data)

    """


@property
    def report_url(self):
        return f"{self.fight.report_url}&source={self.source_id}"

    @property
    def used_spells(self):
        spells = [cast.spell for cast in self.casts]
        return utils.uniqify(spells, key=lambda spell: spell.spell_id)

    def add_cast(self, **kwargs):
        cast = Cast(**kwargs)
        cast.player = self
        self.casts.append(cast)
        return cast
    """
