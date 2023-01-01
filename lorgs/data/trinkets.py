"""On Use Trinkets."""
# pylint: disable=wildcard-import
# pylint: disable=unused-wildcard-import


from typing import Any

from lorgs.data.classes import *
from lorgs.models.wow_spec import WowSpec
from lorgs.models.wow_spell import WowSpell


mythic = "&bonus=6646"


def add_trinket(*specs: WowSpec, **kwargs: Any):
    kwargs.setdefault("spell_type", SpellType.TRINKET)
    kwargs.setdefault("show", False)
    spell = WowSpell(**kwargs)

    for spec in specs:
        spec.add_spells(spell)


################################### DUNGEONS ###################################


add_trinket(
    *AGI_SPECS,
    *STR_SPECS,
    spell_id=383781,
    color="#b34747",
    cooldown=180,
    duration=20,
    name="Algeth'ar Puzzle Box",
    icon="inv_misc_enggizmos_18.jpg",
    wowhead_data=f"item=193701{mythic}&ilvl=372",
)


add_trinket(
    *ALL_SPECS,
    spell_id=215956,
    color="#6b6bb3",
    cooldown=120,
    duration=30,
    name="Horn of Valor",
    icon="inv_misc_horn_03.jpg",
    wowhead_data=f"item=133642{mythic}&ilvl=372",
)


add_trinket(
    *INT_SPECS,
    spell_id=385884,
    color="#cca633",
    cooldown=150,
    duration=20,  # 20sec buff + 20sec debuff
    name="Time-Breaching Talon",
    icon="inv_10_dungeonjewelry_explorer_trinket_3_color3.jpg",
    wowhead_data=f"item=193791{mythic}&ilvl=372",
)


##################################### RAID #####################################

add_trinket(
    *AGI_SPECS,
    *STR_SPECS,
    spell_id=377453,
    color="#53b6bd",
    cooldown=180,
    name="Storm-Eater's Boon",
    icon="inv_10_elementalspiritfoozles_air.jpg",
    wowhead_data=f"item=194302{mythic}&ilvl=421",
)


add_trinket(
    *AGI_SPECS,
    *STR_SPECS,
    spell_id=377463,
    color="#8ec6d4",
    cooldown=120,
    duration=2,
    name="Manic Grieftorch",
    icon="shaman_talent_unleashedfury.jpg",
    wowhead_data=f"item=194308{mythic}&ilvl=424",
)
