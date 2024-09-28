# IMPORT LOCAL LIBRARIES
from lorgs.models import wow_item
from lorgs.models.wow_spell import SpellType


class WowTrinket(wow_item.WowItem):
    """OnUse Trinkets."""

    spell_type: str = SpellType.TRINKET

    color = "#a335ee"  # Epic Items
