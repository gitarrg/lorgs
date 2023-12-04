# IMPORT STANDARD LIBRARIES
from typing import Any

# IMPORT LOCAL LIBRARIES
from lorgs.models import wow_spell
from lorgs.models.wow_spell import SpellType
from lorgs.models.wow_spec import WowSpec


BONUS_ID_MYTHIC = "bonus=6646"


class WowItem(wow_spell.WowSpell):
    """BaseClass for (useable) items such as Trinkets, Potions or anythign else worth tracking."""

    spell_type = SpellType.ITEM
    show = False

    item: int
    """Item ID as seen on wowhead/ingame."""

    ilvl: int = 0
    """Item Level to display in the tooltip."""

    def __init__(self, *specs: WowSpec, **kwargs: Any):
        for spec in specs:
            spec.add_spells(self)

        super().__init__(**kwargs)

    def _gen_wowhead_data(self) -> str:
        parts = []

        if self.item:
            parts.append(f"item={self.item}")
        if self.ilvl > 0:
            parts.append(BONUS_ID_MYTHIC)
            parts.append(f"ilvl={self.ilvl}")

        return "&".join(parts)

    def post_init(self) -> None:
        self.wowhead_data = self._gen_wowhead_data()
        return super().post_init()
