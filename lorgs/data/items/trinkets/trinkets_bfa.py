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
)


################################################################################
# Operation: Mechagon: Junkyard


################################################################################
# Operation: Mechagon: Workshop

INGENIOUS_MANA_BATTERY = WowTrinket(
    spell_id=0,
    name="Ingenious Mana Battery",
    icon="inv_engineering_reavesbattery.jpg",
    item=169344,
)
"""Store Mana and release later

> Use: Channel to store 1224 mana in the Ingenious Mana Battery, up to a max of 4895. (1 Min Cooldown)
> Equip: While your mana is above 50%, gain 3 Versatility, increased by up to 100%
> by the mana stored in the battery. While your mana is under 50%, siphon 50429 mana
> every 5 sec from the Ingenious Mana Battery into your mana pool.
"""


WowTrinket(
    spell_id=0,
    color="#d3d01a",
    cooldown=120,
    name="K.U.-J.0.'s Flame Vents",
    icon="achievement_cooking_masterofthegrill.jpg",
    item=232546,
    ilvl=636,
)
"""On-Use AoE DMG 

> Use: Channel to vent flames for 2 sec, dealing 1583517 Fire damage split between all nearby enemies.
> Mechanical enemies become Superheated, taking 75294  additional Fire damage when struck by your next harmful ability. (2 Min Cooldown)
"""
# Missing Spell ID
# KUJ0S_FLAME_VENTS.add_specs(*AGI_SPECS)
# KUJ0S_FLAME_VENTS.add_specs(*STR_SPECS)


MODULAR_PLATINUM_PLATING = WowTrinket(
    spell_id=299869,
    cooldown=120,
    name="Modular Platinum Plating",
    icon="inv_shield_68.jpg",
    item=232546,
)
"""On-Use Amor.

Buff: 299869

> Use: Gain 4 stacks of Platinum Plating for 30 sec, increasing your Armor by 7.
> Receiving more than 10% of your health from a Physical damage effect will remove one stack of Platinum Plating. (2 Min Cooldown)
"""


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
