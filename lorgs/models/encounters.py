"""Models for Raids and RaidBosses."""
# pylint: disable=too-few-public-methods

# IMPORT THIRD PARTY LIBRARIES
import sqlalchemy as sa

# IMPORT LOCAL LIBRARIES
from lorgs import utils
from lorgs import db
from lorgs.models import base


class RaidZone(db.Base):
    """A raid zone in the Game."""

    __tablename__ = "raid_zone"

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(128))

    bosses = sa.orm.relationship(
        "RaidBoss",
        back_populates="zone",
        cascade="all,save-update,delete",
        # lazy="joined"
    )

    def __repr__(self):
        return f"<RaidZone(id={self.id} name={self.name})>"

    def as_dict(self):
        return {
            "id": self.id,
            "name": self.name,
        }

    @property
    def name_slug(self):
        return utils.slug(self.name, space="-")


class RaidBoss(db.Base, base.IconPathMixin):
    """A raid boss in the Game."""

    __tablename__ = "raid_boss"

    id = sa.Column(sa.Integer, primary_key=True)

    zone = sa.orm.relationship("RaidZone", back_populates="bosses")
    zone_id = sa.Column(sa.Integer, sa.ForeignKey("raid_zone.id", ondelete="cascade"))

    order = sa.Column(sa.Integer)
    name = sa.Column(sa.String(128))

    __mapper_args__ = {
        "order_by" : order
    }

    def __repr__(self):
        return f"<RaidBoss(id={self.id} name={self.name})>"

    def as_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "name_slug": self.name_slug,
        }

    @property
    def name_slug(self):
        return utils.slug(self.name, space="-")

    @property
    def icon_name(self):
        return f"bosses/{self.zone.name_slug}/{self.name_slug}.jpg"
