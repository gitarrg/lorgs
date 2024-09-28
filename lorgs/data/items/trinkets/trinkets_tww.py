from lorgs.data.classes import *
from lorgs.models.wow_trinket import WowTrinket


# AraKara
# no on use trinkets


# City of Threads
# [Oppressive Orator's Larynx] = not worth?


# Dawnbreaker
# [Mereldar's Toll]


# Stonevault
# [High Speaker's Accretion]
# [Overclocked Gear-a-Rang Launcher]
WowTrinket(
    spell_id=443407,
    cooldown=90,
    duration=15,
    name="Skarmorak Shard",
    icon="inv_arathordungeon_fragment_color2.jpg",
    item=219300,
    ilvl=619,
).add_specs(*STR_SPECS)
