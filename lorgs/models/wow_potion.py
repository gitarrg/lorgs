# IMPORT LOCAL LIBRARIES
from lorgs.models import wow_item
from lorgs.models.wow_spell import SpellType


class WowPotion(wow_item.WowItem):
    """Potion or other Consumables with an OnUse-Effect."""

    spell_type = SpellType.POTION

    cooldown = 300  # default cooldown for all potions
