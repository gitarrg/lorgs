"""Define Consumeables/Potions players can use."""
# pylint: disable=line-too-long
# pylint: disable=wildcard-import
# pylint: disable=unused-wildcard-import
# from lorgs.data.classes import *

from lorgs.data.classes import *
from lorgs.models.wow_spell import WowSpell


maxilvl = "&ilvl=252"
mythic = "&bonus=6646"

TYPE_TRINKET = WowSpell.TYPE_TRINKET



# everyone
for s in ALL_SPECS:
    # Dungeon
    s.add_spell(spell_type=TYPE_TRINKET, spell_id=330323, cooldown=180,                 name="Inscrutable Quantum Device",  icon="inv_trinket_80_titan02a.jpg", wowhead_data=f"item=179350{mythic}{maxilvl}")
    s.add_spell(spell_type=TYPE_TRINKET, spell_id=345539, cooldown=180, duration=35,    name="Empyreal Ordnance",           icon="spell_animabastion_nova.jpg", wowhead_data=f"item=180117{mythic}{maxilvl}")

    # pvp badge
    s.add_spell(spell_type=TYPE_TRINKET, spell_id=345228, cooldown=60,  duration=15,    name="Gladiator's Badge",           icon="spell_holy_championsbond.jpg", wowhead_data=f"item=185197&bonus=7315:1518:6646")

    # Other Trinkets
    s.add_spell(spell_type=TYPE_TRINKET, spell_id=348139, cooldown=90,  duration=9,     name="Instructor's Divine Bell",    icon="inv_misc_bell_01.jpg",        wowhead_data="item=184842&&bonus=1472:5894:6646")

# Intellect users
for s in INT_SPECS:
    s.add_spell(spell_type=TYPE_TRINKET, spell_id=345801, cooldown=120, duration=15, name="Soulletting Ruby", icon="inv_jewelcrafting_livingruby_01.jpg", wowhead_data=f"item=178809{mythic}{maxilvl}")
    s.add_spell(spell_type=TYPE_TRINKET, spell_id=355321, cooldown=120, duration=40, name="Shadowed Orb of Torment", icon="spell_animamaw_orb.jpg", wowhead_data=f"item=186428{mythic}{maxilvl}")

# Agility Users
for s in AGI_SPECS:
    s.add_spell(spell_type=TYPE_TRINKET, spell_id=345530, cooldown=90, duration=6, name="Overcharged Anima Battery", icon="inv_battery_01.jpg", wowhead_data=f"item=180116{mythic}{maxilvl}")
    s.add_spell(spell_type=TYPE_TRINKET, spell_id=355333, cooldown=90, duration=20, name="Salvaged Fusion Amplifier", icon="spell_progenitor_missile.jpg", wowhead_data=f"item=186432{mythic}{maxilvl}")

# Strength Users
for s in STR_SPECS:
    s.add_spell(spell_type=TYPE_TRINKET, spell_id=329831, cooldown=90, duration=15, name="Overwhelming Power Crystal", icon="spell_mage_focusingcrystal.jpg", wowhead_data=f"item=179342{mythic}{maxilvl}")


for s in [DRUID_FERAL, HUNTER_SURVIVAL, MONK_BREWMASTER, DRUID_GUARDIAN]:
    # 2h Agi on use weapon https://www.wowhead.com/item=186404/jotungeirr-destinys-call?bonus=7757
    s.add_spell(spell_type=TYPE_TRINKET, spell_id=357773, cooldown=180, duration=30, color="#7f4af0", name="Jotungeirr, Destiny's Call", icon="inv_polearm_2h_mawraid_d_01.jpg", wowhead_data=f"item=186404{mythic}{maxilvl}")


# hide all trinkets by default
for spell in WowSpell.all:
    if spell.spell_type == TYPE_TRINKET:
        spell.show = False
