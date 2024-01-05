"""Define Consumeables/Potions players can use."""
# pylint: disable=line-too-long
# pylint: disable=wildcard-import
# pylint: disable=unused-wildcard-import


from lorgs.data.classes import *
from lorgs.models.wow_potion import WowPotion


################################################################################
# Heal Potions
#

# generic pots for all specs
WowPotion(
    spell_id=6262,
    cooldown=0,  # no cooldown per se. One per fight use.
    color="#63cf48",
    name="Healthstone",
    icon="warlock_-healthstone.jpg",
    item=5512,
).add_specs(*ALL_SPECS)


WowPotion(
    spell_id=370511,
    cooldown=300,
    color="#e35f5f",
    name="Refreshing Healing Potion",
    icon="inv_10_alchemy_bottle_shape4_red.jpg",
    item=191380,
    variations=[
        415569,  # Dreamwalker's Healing Potion
        423414,  # Potion of Withering Dreams
    ],
).add_specs(*ALL_SPECS)


################################################################################
# DPS Potions
#

WowPotion(
    spell_id=371028,
    duration=30,
    color="#297acc",
    name="Elemental Potion of Ultimate Power",
    icon="trade_alchemy_dpotion_b20.jpg",
    item=191383,
    variations=[
        191389,  # Elemental Potion of Power
        371028,
    ],
).add_specs(*ALL_SPECS)


# Intellect users
# for s in INT_SPECS:
#     s.add_spell(spell_type=TYPE_POTION, spell_id=307162, cooldown=300, duration=25, color="#b576e8", name="Potion of Spectral Intellect", icon="trade_alchemy_potionc4.jpg")
#
# # Agility Users
# for s in AGI_SPECS:
#     s.add_spell(spell_type=TYPE_POTION, spell_id=307159, cooldown=300, duration=25, color="#b576e8", name="Potion of Spectral Agility",   icon="trade_alchemy_potionc6.jpg")
#
# # Strength Users
# for s in STR_SPECS:
#     s.add_spell(spell_type=TYPE_POTION, spell_id=307164, cooldown=300, duration=25, color="#b576e8", name="Potion of Spectral Strength",  icon="trade_alchemy_potionc2.jpg")


################################################################################
# Mana Potions
#

WowPotion(
    spell_id=370607,
    color=COL_MANA,
    name="Aerated Mana Potion",
    icon="inv_10_alchemy_bottle_shape1_blue.jpg",
    item=191386,
).add_specs(*HEAL.specs)

WowPotion(
    spell_id=371152,
    duration=10,
    color=COL_MANA,
    name="Potion of Spiritual Clarity",
    icon="inv_10_alchemy_bottle_shape4_green.jpg",
    item=191367,
).add_specs(*HEAL.specs)

WowPotion(
    spell_id=371033,
    duration=10,
    color=COL_MANA,
    name="Potion of Frozen Focus",
    icon="inv_10_alchemy_bottle_shape4_blue.jpg",
    item=191363,
).add_specs(*HEAL.specs)
