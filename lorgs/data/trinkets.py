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

"""
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
"""

################################## S2 DUNGEONS #################################


add_trinket(
    *INT_SPECS,
    spell_id=385884,
    color="#cca633",
    cooldown=150,
    duration=20,  # 20sec buff + 20sec debuff
    name="Time-Breaching Talon",
    icon="inv_10_dungeonjewelry_explorer_trinket_3_color3.jpg",
    wowhead_data=f"item=193791{mythic}&ilvl=441",
)


add_trinket(
    *ALL_SPECS,
    spell_id=383941,
    color="#ab9671",
    cooldown=180,
    duration=20,
    name="Irideus Fragment",
    icon="inv_10_dungeonjewelry_titan_trinket_1facefragment_color3.jpg",
    wowhead_data=f"item=193743{mythic}&ilvl=441",
)


add_trinket(
    *MAGE.specs,
    *WARLOCK.specs,
    PRIEST_SHADOW,
    SHAMAN_ELEMENTAL,
    DRUID_BALANCE,
    EVOKER_DEVASTATION,
    spell_id=381768,
    color="#5dcdde",
    cooldown=120,
    duration=20,
    name="Spoils of Neltharus",
    icon="inv_10_dungeonjewelry_dragon_trinket_4_bronze.jpg",
    wowhead_data=f"item=193773{mythic}&ilvl=441",
)


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


############################### 10.1 Megadungeon ###############################

add_trinket(
    *HEAL.specs,
    spell_id=417939,
    color="#ff8a1d",
    cooldown=120,
    name="Echoing Tyrstone",
    icon="ability_paladin_lightofthemartyr.jpg",
    wowhead_data=f"item=207552{mythic}&ilvl=441",
)

add_trinket(
    *RDPS.specs,
    *MDPS.specs,
    spell_id=418527,
    color="#40d1be",
    duration=20,
    cooldown=180,
    name="Mirror of Fractured Tomorrows",
    icon="achievement_dungeon_ulduarraid_misc_06.jpg",
    wowhead_data=f"item=207581{mythic}&ilvl=441",
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


################################# S3 Dungeons ##################################

add_trinket(
    *AGI_SPECS,
    spell_id=265954,
    color="#d3d01a",
    cooldown=90,
    name="My'das Talisman",
    icon="inv_offhand_draenei_a_02.jpg",
    wowhead_data=f"item=158319{mythic}&ilvl=483",
)

add_trinket(
    *AGI_SPECS,
    spell_id=429257,
    color="#39d31a",
    cooldown=90,
    name="Witherbark's Branch",
    icon="inv_misc_branch_01.jpg",
    wowhead_data=f"item=109999{mythic}&ilvl=483",
)


# tracking via buff, since there does not seem to be a cast associated with the trinket
balefire_branch = WowSpell(
    spell_id=268998,
    color="#8434df",
    spell_type=SpellType.TRINKET,
    cooldown=90,
    name="Balefire Branch",
    icon="inv_staff_26.jpg",
    wowhead_data=f"item=159630{mythic}&ilvl=483",
    show=False,
    event_type="applybuff",
)
for spec in INT_SPECS:
    spec.add_buff(balefire_branch)


################################### T35 RAID ###################################

add_trinket(
    *ALL_SPECS,
    spell_id=423611,
    color="#eb3838",
    duration=20,
    cooldown=120,
    name="Ashes of the Embersoul",
    icon="sha_spell_fire_felfire_nightmare.jpg",
    wowhead_data=f"item=207167{mythic}&ilvl=483",
)

add_trinket(
    *AGI_SPECS,
    spell_id=422303,
    color="#eb3838",
    duration=3,
    cooldown=90,
    name="Bandolier of Twisted Blades",
    icon="inv_cape_special_knifebandolier_c_01.jpg",
    wowhead_data=f"item=207165{mythic}&ilvl=483",
)

add_trinket(
    *INT_SPECS,
    spell_id=422146,
    color="#eb8938",
    duration=12,
    cooldown=120,
    name="Belor'relos, the Suncaller",
    icon="inv_wand_1h_firelandsraid_d_01.jpg",
    wowhead_data=f"item=207172{mythic}&ilvl=483",
)

add_trinket(
    *INT_SPECS,
    spell_id=422956,
    color="#9c67f1",
    duration=18,
    cooldown=120,
    name="Nymue's Unraveling Spindle",
    icon="inv_cloth_outdooremeralddream_d_01_buckle.jpg",
    wowhead_data=f"item=208615{mythic}&ilvl=483",
)

# TODO:
# [Branch of the Tormented Ancient] = STR
# [Fyrakk's Tainted Rageheart]
