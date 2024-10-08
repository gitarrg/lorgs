from lorgs.data.classes import *
from lorgs.models.wow_trinket import WowTrinket


WowTrinket(
    spell_id=383781,
    color="#b34747",
    cooldown=180,
    duration=20,
    name="Algeth'ar Puzzle Box",
    icon="inv_misc_enggizmos_18.jpg",
    item=193701,
    ilvl=372,
    query=False,
).add_specs(
    *AGI_SPECS,
    *STR_SPECS,
)


WowTrinket(
    spell_id=385884,
    color="#cca633",
    cooldown=150,
    duration=20,  # 20sec buff + 20sec debuff
    name="Time-Breaching Talon",
    icon="inv_10_dungeonjewelry_explorer_trinket_3_color3.jpg",
    item=193791,
    ilvl=447,
    query=False,
).add_specs(*INT_SPECS)


WowTrinket(
    spell_id=383941,
    color="#ab9671",
    cooldown=180,
    duration=20,
    name="Irideus Fragment",
    icon="inv_10_dungeonjewelry_titan_trinket_1facefragment_color3.jpg",
    item=193743,
    ilvl=447,
    query=False,
).add_specs(*ALL_SPECS)


# tracked for all INT-DPS-Specs
WowTrinket(
    spell_id=381768,
    color="#5dcdde",
    cooldown=120,
    duration=20,
    name="Spoils of Neltharus",
    icon="inv_10_dungeonjewelry_dragon_trinket_4_bronze.jpg",
    item=193773,
    ilvl=447,
    query=False,
).add_specs(*INT_DPS_SPECS)


############################### 10.1 Megadungeon ###############################

WowTrinket(
    spell_id=417939,
    color="#ff8a1d",
    cooldown=120,
    name="Echoing Tyrstone",
    icon="ability_paladin_lightofthemartyr.jpg",
    item=207552,
    ilvl=483,
    query=False,
).add_specs(*HEAL.specs)


WowTrinket(
    spell_id=418527,
    color="#40d1be",
    duration=20,
    cooldown=180,
    name="Mirror of Fractured Tomorrows",
    icon="achievement_dungeon_ulduarraid_misc_06.jpg",
    item=207581,
    ilvl=483,
    query=False,
).add_specs(*DPS_SPECS)


WowTrinket(
    spell_id=419278,
    color="#e7c21f",
    cooldown=180,
    name="Iridal, the Earth's Master",
    icon="inv_staff_2h_dracthyr_c_01.jpg",
    item=208321,
    ilvl=483,
    query=False,
).add_specs(*INT_SPECS)
