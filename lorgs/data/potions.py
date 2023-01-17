"""Define Consumeables/Potions players can use."""
# pylint: disable=line-too-long
# pylint: disable=wildcard-import
# pylint: disable=unused-wildcard-import
# fmt: off
from typing import Any

from lorgs.data.classes import *
from lorgs.models.wow_spell import WowSpell


# alias
TYPE_POTION = SpellType.POTION


def add_potion(*specs: WowSpec, **kwargs: Any):
    kwargs.setdefault("spell_type", SpellType.POTION)
    kwargs.setdefault("cooldown", 300)
    kwargs.setdefault("show", False)
    spell = WowSpell(**kwargs)

    for spec in specs:
        spec.add_spells(spell)


################################################################################
# Potions
#

# generic pots for all specs
add_potion(
    *ALL_SPECS,
    spell_id=6262,
    cooldown=0,  # no cooldown per se. One per fight use.
    color="#63cf48",
    name="Healthstone",
    icon="warlock_-healthstone.jpg",
    wowhead_data="item=5512"
)


add_potion(*ALL_SPECS,
    spell_id=370511,
    cooldown=300,
    color="#e35f5f",
    name="Refreshing Healing Potion",
    icon="inv_10_alchemy_bottle_shape4_red.jpg",
    wowhead_data="item=191380"
)


add_potion(
    *ALL_SPECS,
    spell_id=371024,
    duration=30,
    color="#297acc",
    name="Elemental Potion of Power",
    icon="trade_alchemy_dpotion_b10.jpg",
    wowhead_data="item=191389"
)


add_potion(
    *ALL_SPECS,
    spell_id=371028,
    duration=30,
    color="#297acc",
    name="Elemental Potion of Ultimate Power",
    icon="trade_alchemy_dpotion_b20.jpg",
    wowhead_data="item=191383"
)


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

# Heal Classes
for s in HEAL.specs:
    # TODO: track all ranks? (or maybe rank3 only.. those IDs are afaik r2)
    s.add_spell(spell_type=TYPE_POTION, spell_id=370607, cooldown=300,              color=COL_MANA,  name="Aerated Mana Potion",        icon="inv_10_alchemy_bottle_shape1_blue.jpg", wowhead_data="item=191386")
    s.add_spell(spell_type=TYPE_POTION, spell_id=371152, cooldown=300, duration=10, color=COL_MANA,  name="Potion of Spiritual Clarity",  icon="inv_10_alchemy_bottle_shape4_green.jpg", wowhead_data="item=191367")
    s.add_spell(spell_type=TYPE_POTION, spell_id=371033, cooldown=300, duration=10, color=COL_MANA,  name="Potion of Frozen Focus",  icon="inv_10_alchemy_bottle_shape4_blue.jpg", wowhead_data="item=191363")


# hide all potions by default
for spell in WowSpell.list():
    if spell.spell_type in (TYPE_POTION, ):
        spell.show = False
