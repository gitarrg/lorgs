from lorgs.data.classes import *
from lorgs.models.wow_trinket import WowTrinket


ELEMENTIUM_POCKET_ANVIL = WowTrinket(
    *AGI_SPECS,
    *STR_SPECS,
    spell_id=401306,
    color="#66ad96",
    cooldown=60,
    name="Elementium Pocket Anvil",
    icon="inv_blacksmithing_khazgoriananvil.jpg",
    item=202617,
    ilvl=447,
    query=False,
)


BEACON_TO_THE_BEYOND = WowTrinket(
    *ALL_SPECS,
    spell_id=402583,
    color="#6e38eb",
    cooldown=150,
    name="Beacon to the Beyond",
    icon="inv_cosmicvoid_orb.jpg",
    item=203963,
    ilvl=450,
    query=False,
)
