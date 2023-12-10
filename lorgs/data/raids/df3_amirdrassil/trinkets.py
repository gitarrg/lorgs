from lorgs.data.classes import *
from lorgs.models.wow_trinket import WowTrinket


WowTrinket(
    *ALL_SPECS,
    spell_id=423611,
    color="#eb3838",
    duration=20,
    cooldown=120,
    name="Ashes of the Embersoul",
    icon="sha_spell_fire_felfire_nightmare.jpg",
    item=207167,
    ilvl=483,
)


WowTrinket(
    *AGI_SPECS,
    spell_id=422303,
    color="#eb3838",
    duration=3,
    cooldown=90,
    name="Bandolier of Twisted Blades",
    icon="inv_cape_special_knifebandolier_c_01.jpg",
    item=207165,
    ilvl=483,
)


WowTrinket(
    *INT_SPECS,
    spell_id=422146,
    color="#eb8938",
    duration=12,
    cooldown=120,
    name="Belor'relos, the Suncaller",
    icon="inv_wand_1h_firelandsraid_d_01.jpg",
    item=207172,
    ilvl=483,
)


WowTrinket(
    *INT_SPECS,
    spell_id=422956,
    color="#9c67f1",
    duration=18,
    cooldown=120,
    name="Nymue's Unraveling Spindle",
    icon="inv_cloth_outdooremeralddream_d_01_buckle.jpg",
    item=208615,
    ilvl=483,
)


WowTrinket(
    *HEAL.specs,
    spell_id=422083,
    color="#5ac927",
    duration=12 + 12,  # 12sec Seed + 12sec Mastery
    cooldown=120,
    name="Smoldering Seedling",
    icon="inv_treepet.jpg",
    item=207170,
    ilvl=483,
)
