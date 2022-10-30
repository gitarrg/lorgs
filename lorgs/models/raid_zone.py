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

    def __init__(self, id: int, name: str, bosses: list[RaidBoss] = []):
        self.id: int = id
        """ID of the Raid Zone. aka. T28, T29 (as used in WarcraftLogs)."""
        self.name: str = name
        """Full Name of the Zone. eg.: `Castle Nathria`."""
        self.bosses = bosses
        """All Bosses, in order, in this Zone."""
        self.name_slug = utils.slug(self.name, space="-")

    def __repr__(self):
        return f"<RaidZone(id={self.id} name={self.name})>"

    def as_dict(self) -> dict[str, typing.Any]:
        return {
            "id": self.id,
            "name": self.name,
            "name_slug": self.name_slug,
            "bosses": [boss.as_dict() for boss in self.bosses]  # list to preserve the correct order
        }

    def add_boss(self, boss: typing.Optional[RaidBoss] = None, **kwargs: typing.Any) -> RaidBoss:
        """Add a new RaidBoss to this zone."""
        boss = boss or RaidBoss(**kwargs)
        self.bosses.append(boss)
        return boss

    def add_bosses(self, *bosses: RaidBoss) -> None:
        """Add multiple Bosses to this Zone."""
        self.bosses.extend(bosses)
