"""Defines a Raid in the Game."""
# pylint: disable=too-few-public-methods

# IMPORT STANDARD LIBRARIES
import typing

# IMPORT LOCAL LIBRARIES
from lorgs import utils
from lorgs.models import base
from lorgs.models.raid_boss import RaidBoss


class RaidZone(base.Model):
    """A raid zone in the Game."""

    def __init__(self, id, name):
        self.id: int = id
        self.name: str = name
        self.bosses: typing.List[RaidBoss] = []

        self.name_slug = utils.slug(self.name, space="-")

    def __repr__(self):
        return f"<RaidZone(id={self.id} name={self.name})>"

    def as_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "name_slug": self.name_slug,
            "bosses": [boss.as_dict() for boss in self.bosses]  # list to preserve the correct order
        }

    def add_boss(self, **kwargs) -> RaidBoss:
        """Add a new RaidBoss to this zone."""
        boss = RaidBoss(zone=self, **kwargs)
        self.bosses.append(boss)
        return boss
