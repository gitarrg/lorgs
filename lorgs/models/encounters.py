"""Models for Raids and RaidBosses."""
# pylint: disable=too-few-public-methods

# IMPORT THIRD PARTY LIBRARIES
import sqlalchemy
import flask

# IMPORT LOCAL LIBRARIES
from lorgs import utils
from lorgs.db import db


class RaidZone(db.Model):
    """A raid zone in the Game."""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))

    bosses = sqlalchemy.orm.relationship(
        "RaidBoss",
        back_populates="zone",
        cascade="all,save-update,delete",
    )

    def __repr__(self):
        return f"<RaidZone({self.name})>"

    @property
    def name_slug(self):
        return utils.slug(self.name, space="-")


class RaidBoss(db.Model):
    """A raid boss in the Game."""

    id = db.Column(db.Integer, primary_key=True)  # id to maintain order of creation

    zone = sqlalchemy.orm.relationship("RaidZone", back_populates="bosses")
    zone_id = db.Column(db.Integer, db.ForeignKey("raid_zone.id", ondelete="cascade"))

    boss_id = db.Column(db.Integer, index=True) # ingame id
    name = db.Column(db.String(128))

    fights = sqlalchemy.orm.relationship("Fight", back_populates="boss")

    def __repr__(self):
        return f"<RaidBoss({self.name})>"

    @property
    def name_slug(self):
        return utils.slug(self.name, space="-")

    @property
    def img_path(self):
        filename = f"images/bosses/{self.zone.name_slug}/{self.name_slug}.jpg"
        return flask.url_for("static", filename=filename)
