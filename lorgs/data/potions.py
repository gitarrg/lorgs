"""Define Consumeables/Potions players can use."""
# pylint: disable=line-too-long
# pylint: disable=bad-whitespace
# pylint: disable=wildcard-import
# pylint: disable=unused-wildcard-import
from lorgs.data.classes import *
from lorgs.models.wow_spell import WowSpell


# alias
TYPE_POTION = WowSpell.TYPE_POTION

# generic pots for all specs
for s in ALL_SPECS:
    s.add_spell(spell_type=TYPE_POTION, spell_id=6262,                              color="#63cf48", name="Healthstone",                  icon="warlock_-healthstone.jpg", wowhead_data="item=5512")
    s.add_spell(spell_type=TYPE_POTION, spell_id=307192, cooldown=300,              color="#e35f5f", name="Spiritual Healing Potion",     icon="inv_alchemy_70_red.jpg",   wowhead_data="item=171267")
    s.add_spell(spell_type=TYPE_POTION, spell_id=307495, cooldown=300, duration=25, color="#57bd8b", name="Potion of Phantom Fire",       icon="inv_alchemy_90_combat1_green.jpg")

    # not a potion.. but for now, this works
    s.add_buff(PRIEST_POWER_INFUSION)  # 10060
    s.add_buff(TIMEWARP)        # 80353
    s.add_buff(BLOODLUST)       # 2825
    s.add_buff(HEROISM)         # 32182


# Intellect users
for s in INT_SPECS:
    s.add_spell(spell_type=TYPE_POTION, spell_id=307162, cooldown=300, duration=25, color="#b576e8", name="Potion of Spectral Intellect", icon="trade_alchemy_potionc4.jpg")

# Agility Users
for s in AGI_SPECS:
    s.add_spell(spell_type=TYPE_POTION, spell_id=307159, cooldown=300, duration=25, color="#b576e8", name="Potion of Spectral Agility",   icon="trade_alchemy_potionc6.jpg")

# Strength Users
for s in STR_SPECS:
    s.add_spell(spell_type=TYPE_POTION, spell_id=307164, cooldown=300, duration=25, color="#b576e8", name="Potion of Spectral Strength",  icon="trade_alchemy_potionc2.jpg")

# Heal Classes
for s in HEAL.specs:
    s.add_spell(spell_type=TYPE_POTION, spell_id=307161, cooldown=300, duration=10, color=COL_MANA,  name="Potion of Spiritual Clarity",  icon="inv_alchemy_80_elixir01orange.jpg")
    s.add_spell(spell_type=TYPE_POTION, spell_id=307193, cooldown=300,              color=COL_MANA,  name="Spiritual Mana Potion",        icon="inv_alchemy_70_blue.jpg")


# hide all potions by default
for spell in WowSpell.all:
    if spell.spell_type == TYPE_POTION:
        spell.show = False
