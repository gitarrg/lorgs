"""Models for Warcraftlog-Reports/Fights/Actors."""

# pylint: disable=too-few-public-methods

# IMPORT STANRD LIBRARIES
# import datetime
# import arrow
# import textwrap

# IMPORT THIRD PARTY LIBRARIES
# import sqlalchemy
import sqlalchemy as sa
# from sqlalchemy import sa.Column, sa.ForeignKey
# from sqlalchemy import sa.Integer, String, Bigsa.Integer, sa.Unicode, Float
# from sqlalchemy.orm import sa.orm.relationship

# IMPORT LOCAL LIBRARIES
from lorgs import db
from lorgs import utils
# from lorgs.cache import Cache
# from lorgs.client import WarcraftlogsClient
# from lorgs.logger import logger
# from lorgs.models import base
# from lorgs.models.encounters import RaidBoss
# from lorgs.models.encounters import RaidZone
# from lorgs.models.specs import WowClass
# from lorgs.models.specs import WowSpec
# from lorgs.models.specs import WowSpell


class Report(db.Base):
    """docstring for Fight"""

    __tablename__ = "report"

    # attributes
    report_id = sa.Column(sa.String(64), primary_key=True)
    start_time = sa.Column(sa.BigInteger, default=0)
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

    """
    def __init__(self, report_id: str):
        self.report_id = report_id
        self.title = ""
        self.start_time = 0
        self.zone = None
        self.fights = []
    """

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

    @property
    def players(self):
        players = utils.flatten(fight.players for fight in self.fights)
        return utils.uniqify(players, key=lambda player: player.source_id)
    """

    @property
    def used_spells(self):
        spells = utils.flatten(fight.used_spells for fight in self.fights)
        return utils.uniqify(spells, key=lambda spell: spell.spell_id)
    """


class Fight(db.Base):
    """Basically a pull."""

    __tablename__ = "report_fight"

    # attributes
    # id = sa.Column(sa.Integer, primary_key=True)
    fight_id = sa.Column(sa.Integer, primary_key=True)
    start_time = sa.Column(sa.BigInteger)
    end_time = sa.Column(sa.BigInteger)
    percent = sa.Column(sa.Float, default=0)

    # sa.orm.relationships
    report_id = sa.Column(sa.String(64), sa.ForeignKey("report.report_id", ondelete="cascade"), primary_key=True)
    report = sa.orm.relationship("Report", back_populates="fights")

    boss_id = sa.Column(sa.Integer, sa.ForeignKey("raid_boss.id"))
    boss = sa.orm.relationship("RaidBoss")

    # children
    players = sa.orm.relationship(
        "Player",
        back_populates="fight",
        cascade="all,delete,delete-orphan",
        lazy="joined"
    )
    # casts = association_proxy("players", "casts")

    def __repr__(self):
        return f"Fight({self.report_id}, id={self.fight_id}, players={len(self.players)})"

    def as_dict(self):
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

    """
    @property
    def used_spells(self):
        spells = utils.flatten(player.used_spells for player in self.players)
        return utils.uniqify(spells, key=lambda spell: spell.spell_id)
    """

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


class Player(db.Base):
    """a player in a given fight.

    TODO:
        rename to actor?

    """
    __tablename__ = "report_player"

    id = sa.Column(sa.Integer, primary_key=True)

    # the actual player
    source_id = sa.Column(sa.Integer)  # TODO: rename?
    name = sa.Column(sa.Unicode(12)) # names can be max 12 chars
    total = sa.Column(sa.Integer)

    fight_id = sa.Column(sa.Integer, sa.ForeignKey("report_fight.fight_id", ondelete="cascade"))
    fight = sa.orm.relationship("Fight", back_populates="players")

    casts = sa.orm.relationship(
        "Cast",
        back_populates="player",
        cascade="all,delete,delete-orphan",
        lazy="joined"
    )

    # report = association_proxy("fight", "report")
    spec = sa.orm.relationship("WowSpec")
    spec_id = sa.Column(sa.Integer, sa.ForeignKey("wow_spec.id"))


    """
    def __init__(self, source_id=0, name="", total=0, **kwargs):
        super().__init__()
        self.source_id = source_id
        self.name = name
        self.total = total

        self.fight = None

        spec_name = kwargs.get("spec")
        self.spec = WowSpec.get(full_name_slug=spec_name) if spec_name else None

        self.casts = []
        for cast_data in kwargs.get("casts", []):
            self.add_cast(**cast_data)

    """
    def __repr__(self):
        return f"Player({self.name} spec=TODO id={self.source_id} casts={len(self.casts)})"

    """
    def __setstate__(self, state):
        self.source_id = state["source_id"]
        self.name = state["name"]
        self.total = state["total"]

        spec_name = state.get("spec")
        self.spec = WowSpec.get(full_name_slug=spec_name) if spec_name else None

        self.casts = []
        for cast_data in state.get("casts", []):
            self.add_cast(**cast_data)

    def as_dict(self):
        return {
            "source_id": self.source_id,
            "name": self.name,
            "total": self.total,
            "spec": self.spec.full_name_slug if self.spec else "",
            "casts": [cast.as_dict() for cast in self.casts]
        }

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


class Cast(db.Base):
    """docstring for Cast"""

    __tablename__ = "report_cast"

    id = sa.Column(sa.Integer, primary_key=True)
    timestamp = sa.Column(sa.Integer)

    player_id = sa.Column(sa.Integer, sa.ForeignKey(Player.id, ondelete="cascade"))
    player = sa.orm.relationship("Player", back_populates="casts")

    # parent player
    spell = sa.orm.relationship("WowSpell")
    spell_id = sa.Column(sa.Integer, sa.ForeignKey("wow_spell.spell_id"))

    def __repr__(self):
        time_fmt = utils.format_time(self.time)
        return f"Cast({self.spell_id}, at={time_fmt})"

    def as_dict(self):
        return {
            "timestamp": self.timestamp,
            "spell_id": self.spell.spell_id if self.spell else 0,
        }
