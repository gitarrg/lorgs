# IMPORT LOCAL LIBRARIES
from lorgs.models import base
from lorgs.models.dungeon import Dungeon
from lorgs.models.raid_zone import RaidZone


class Season(base.MemoryModel):
    """A Season in the Game."""

    ilvl: int
    """Max Item Level of the Season."""

    raids: list[RaidZone] = []
    """Raids of the Season."""

    dungeons: list[Dungeon] = []
    """Dungeon which part of the Seasons M+ Pool."""
