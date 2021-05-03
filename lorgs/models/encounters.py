"""Models for Raids and RaidBosses."""
# pylint: disable=too-few-public-methods

# IMPORT LOCAL LIBRARIES
from lorgs import utils
from lorgs.models import base


class RaidZone(base.Model):
    """A raid zone in the Game."""

    def __init__(self, id, name):
        super().__init__()

        #: int
        self.id = id

        #: str
        self.name = name

        #: list[<RaidBoss>]
        self.bosses = []

        #: str
        self.name_slug = utils.slug(self.name, space="-")

    def __repr__(self):
        return f"<RaidZone(id={self.id} name={self.name})>"

    def add_boss(self, **kwargs):
        boss = RaidBoss(zone=self, **kwargs)
        self.bosses.append(boss)

    def as_dict(self):
        return {
            "id": self.id,
            "name": self.name,
        }


class RaidBoss(base.Model):
    """A raid boss in the Game."""

    def __init__(self, zone, id, name):
        super().__init__()
        self.id = id
        self.name = name
        self.zone = zone

        self.name_slug = utils.slug(self.name, space="-")
        self.icon_name = f"bosses/{self.zone.name_slug}/{self.name_slug}.jpg"

    def __repr__(self):
        return f"<RaidBoss({self.name})>"

    def as_dict(self):
        return {
            "id": self.id,
            "name": self.name,
        }
