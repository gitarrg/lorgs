from lorgs.data.classes import *
from lorgs.models.wow_trinket import WowTrinket


# Grim Batol
# [Corrupted Egg Shell]

WowTrinket(
    spell_id=92099,
    cooldown=120,
    duration=20,
    name="Skardyn's Grace",
    icon="inv_misc_coin_08.jpg",
    item=133282,
    ilvl=619,
).add_specs(*AGI_SPECS)


WowTrinket(
    spell_id=91374,
    cooldown=90,
    duration=15,
    name="Mark of Khardros",
    icon="inv_hammer_04.jpg",
    item=133300,
    ilvl=619,
).add_specs(*STR_SPECS)
