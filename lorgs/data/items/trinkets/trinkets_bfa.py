from lorgs.data.classes import *
from lorgs.models.wow_trinket import WowTrinket


################################################################################
# Atal Dazar

WowTrinket(
    spell_id=265954,
    color="#d3d01a",
    cooldown=90,
    name="My'das Talisman",
    icon="inv_offhand_draenei_a_02.jpg",
    item=158319,
    ilvl=483,
    query=False,
).add_specs(*AGI_SPECS)


################################################################################
# Operation: Mechagon: Junkyard


################################################################################
# Operation: Mechagon: Workshop

# [Ingenious Mana Battery]

KUJ0S_FLAME_VENTS = WowTrinket(
    spell_id=0,
    color="#d3d01a",
    cooldown=120,
    name="K.U.-J.0.'s Flame Vents",
    icon="achievement_cooking_masterofthegrill.jpg",
    item=232546,
    ilvl=636,
    query=False,  # Need to find spell ID first
)
"""On-Use AoE DMG 

> Use: Channel to vent flames for 2 sec, dealing 1583517 Fire damage split between all nearby enemies.
> Mechanical enemies become Superheated, taking 75294  additional Fire damage when struck by your next harmful ability. (2 Min Cooldown)
"""
# Missing Spell ID
# KUJ0S_FLAME_VENTS.add_specs(*AGI_SPECS)
# KUJ0S_FLAME_VENTS.add_specs(*STR_SPECS)


# [Modular Platinum Plating]


################################################################################
# The MOTHERLODE!!!

# [Azerokk's Resonating Heart]
# [Razdunk's Big Red Button]


################################################################################
# The Underrot

WowTrinket(
    spell_id=268836,
    event_type="applybuff",
    color="#ba5bb5",
    cooldown=90,
    duration=18,
    name="Vial of Animated Blood",
    icon="inv_misc_food_legion_leyblood.jpg",
    item=159625,
    ilvl=372,
    query=False,
).add_specs(*STR_SPECS)


################################################################################
# Waycrest Manor


WowTrinket(
    spell_id=268998,
    event_type="applybuff",
    color="#8434df",
    cooldown=90,
    name="Balefire Branch",
    icon="inv_staff_26.jpg",
    show=False,
    item=159630,
    ilvl=483,
    query=False,
).add_specs(*INT_SPECS)
