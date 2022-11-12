"""Defines a Raid in the Game."""
# pylint: disable=too-few-public-methods

# IMPORT STANDARD LIBRARIES
import typing

# IMPORT LOCAL LIBRARIES
from lorgs import utils
from lorgs.models import base
from lorgs.models.raid_boss import RaidBoss


class RaidZone(base.MemoryModel):
    """A raid zone in the Game."""

    id: int
    """ID of the Raid Zone. aka. T28, T29 (as used in WarcraftLogs)."""

    name: str
    """Full Name of the Zone. eg.: `Castle Nathria`."""

    bosses: list[RaidBoss] = []
    """All Bosses, in order, in this Zone."""

    @property
    def name_slug(self) -> str:
        return utils.slug(self.name, space="-")

    def __repr__(self) -> str:
        return f"<RaidZone(id={self.id} name={self.name})>"

    def as_dict(self) -> dict[str, typing.Any]:
        return {
            "id": self.id,
            "name": self.name,
            "name_slug": self.name_slug,
            "bosses": [boss.as_dict() for boss in self.bosses],
        }

    def add_boss(self, boss: typing.Optional[RaidBoss] = None, **kwargs: typing.Any) -> RaidBoss:
        """Add a new RaidBoss to this zone."""
        boss = boss or RaidBoss(**kwargs)
        self.bosses.append(boss)
        return boss

    def add_bosses(self, *bosses: RaidBoss) -> None:
        """Add multiple Bosses to this Zone."""
        self.bosses.extend(bosses)
