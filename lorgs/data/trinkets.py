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


################################## S1 DUNGEONS #################################


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


################################## S2 DUNGEONS #################################


# Vial of Animated Blood
# tracking via buff, since there does not seem to be a cast associated with the trinket
vial_of_animated_blood = WowSpell(
    spell_id=268836,
    color="#ba5bb5",
    spell_type=SpellType.TRINKET,
    cooldown=90,
    duration=18,
    name="Vial of Animated Blood",
    icon="inv_misc_food_legion_leyblood.jpg",
    wowhead_data=f"item=159625{mythic}&ilvl=372",
    show=False,
    event_type="applybuff",
)
for spec in STR_SPECS:
    spec.add_buff(vial_of_animated_blood)


################################### T31 RAID ###################################

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


add_trinket(
    EVOKER_DEVASTATION,
    EVOKER_PRESERVATION,
    spell_id=394927,
    color="#af4dff",
    cooldown=180,
    duration=3,
    name="Kharnalex, The First Light",
    icon="inv_staff_2h_dragondungeon_c_02.jpg",
    wowhead_data=f"item=195519{mythic}&ilvl=424",
)


################################### T33 RAID ###################################

add_trinket(
    *AGI_SPECS,
    *STR_SPECS,
    spell_id=401306,
    color="#66ad96",
    cooldown=60,
    name="Elementium Pocket Anvil",
    icon="inv_blacksmithing_khazgoriananvil.jpg",
    wowhead_data=f"item=202617{mythic}&ilvl=441",
)

add_trinket(
    *ALL_SPECS,
    spell_id=402583,
    color="#6e38eb",
    cooldown=150,
    name="Beacon to the Beyond",
    icon="inv_cosmicvoid_orb.jpg",
    wowhead_data=f"item=203963{mythic}&ilvl=450",
)
