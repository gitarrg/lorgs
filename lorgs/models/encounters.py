"""Models for Raids and RaidBosses."""
# pylint: disable=too-few-public-methods

# IMPORT LOCAL LIBRARIES
from lorgs import utils
from lorgs.models import base


class RaidZone(base.Model):
    """A raid zone in the Game."""

    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.bosses = []

        self.name_slug = utils.slug(self.name, space="-")

    def __repr__(self):
        return f"<RaidZone(id={self.id} name={self.name})>"

    def as_dict(self):
        return {
            "id": self.id,
            "name": self.name,
        }

    def add_boss(self, **kwargs):
        boss = RaidBoss(zone=self, **kwargs)
        self.bosses.append(boss)
        return boss


class RaidBoss(base.Model):
    """A raid boss in the Game."""

    def __init__(self, zone, id, name):
        self.id = id
        self.zone = zone
        self.name = name

        self.name_slug = utils.slug(self.name, space="-")
        self.icon_name = f"bosses/{self.zone.name_slug}/{self.name_slug}.jpg"

    def __repr__(self):
        return f"<RaidBoss(id={self.id} name={self.name})>"

    def as_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            # "name_slug": self.name_slug,
        }
