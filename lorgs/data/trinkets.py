"""Define Consumeables/Potions players can use."""
# pylint: disable=line-too-long
# pylint: disable=wildcard-import
# pylint: disable=unused-wildcard-import
# from lorgs.data.classes import *

from lorgs.data.classes import *
from lorgs.models.wow_spell import WowSpell, EventType


maxilvl = "&ilvl=278"
mythic = "&bonus=6646"

TYPE_TRINKET = WowSpell.TYPE_TRINKET


########################################################################################################################


#### Dungeons ####
RUBY            = WowSpell(spell_type=TYPE_TRINKET, spell_id=345801, cooldown=120, duration=15, color="#c23636", name="Soulletting Ruby", icon="inv_jewelcrafting_livingruby_01.jpg", wowhead_data=f"item=178809{mythic}{maxilvl}")
POWER_CRYSTAL   = WowSpell(spell_type=TYPE_TRINKET, spell_id=329831, cooldown=90,  duration=15, color="#955fc7", name="Overwhelming Power Crystal", icon="spell_mage_focusingcrystal.jpg", wowhead_data=f"item=179342{mythic}{maxilvl}")

# Dungeon
IQD             = WowSpell(spell_type=TYPE_TRINKET, spell_id=330323, cooldown=180, duration=25, color="#cf8e48", name="Inscrutable Quantum Device", icon="inv_trinket_80_titan02a.jpg", wowhead_data=f"item=179350{mythic}{maxilvl}")
ORDNANCE        = WowSpell(spell_type=TYPE_TRINKET, spell_id=345539, cooldown=180, duration=35, color="#48cfc8", name="Empyreal Ordnance", icon="spell_animabastion_nova.jpg", wowhead_data=f"item=180117{mythic}{maxilvl}")

# s.add_spell(spell_type=TYPE_TRINKET, spell_id=345530, cooldown=90, duration=6, name="Overcharged Anima Battery", icon="inv_battery_01.jpg", wowhead_data=f"item=180116{mythic}{maxilvl}")
# s.add_spell(spell_type=TYPE_TRINKET, spell_id=355333, cooldown=90, duration=20, name="Salvaged Fusion Amplifier", icon="spell_progenitor_missile.jpg", wowhead_data=f"item=186432{mythic}{maxilvl}")

#### RAID ####
# T28
ORB_OF_TORMENT  = WowSpell(spell_type=TYPE_TRINKET, spell_id=355321, cooldown=120, duration=40, color="#8ec6d4", name="Shadowed Orb of Torment", icon="spell_animamaw_orb.jpg", wowhead_data=f"item=186428{mythic}&ilvl=252")

# T29
THE_FIRST_SIGIL = WowSpell(spell_type=TYPE_TRINKET, spell_id=367241, cooldown=300, duration=20, color="#cf5225", name="The First Sigil", icon="inv_legendary_sigilofwisdom.jpg", wowhead_data=f"item=188271{mythic}{maxilvl}")
EARTHBREAKERS   = WowSpell(spell_type=TYPE_TRINKET, spell_id=367808, cooldown=180, duration=12, color="#bf9228", name="Earthbreaker's Impact", icon="spell_nature_earthquake.jpg", wowhead_data=f"item=188264{mythic}{maxilvl}")

# Tracked as three different Buffs/Spells
CACHE_OF_ACQUIRED_TREASURES_AXE   = WowSpell(spell_type=TYPE_TRINKET, spell_id=368650, duration=25, cooldown=180, color="#cc4343", name="Cache of Acquired Treasures (Axe)",   icon="inv_axe_1h_pvp400_c_01.jpg", wowhead_data=f"item=188265{mythic}{maxilvl}")
CACHE_OF_ACQUIRED_TREASURES_SWORD = WowSpell(spell_type=TYPE_TRINKET, spell_id=368649, duration=25, cooldown=180, color="#cca843", name="Cache of Acquired Treasures (Sword)", icon="inv_sword_1h_draenorcrafted_d_01_c_alliance.jpg", wowhead_data=f"item=188265{mythic}{maxilvl}")
# track Wand via the "damage" event
CACHE_OF_ACQUIRED_TREASURES_WAND  = WowSpell(spell_type=TYPE_TRINKET, spell_id=368653,              cooldown=180, color="#43ccb5", name="Cache of Acquired Treasures (Wand)",  icon="inv_wand_25.jpg", wowhead_data=f"item=188265{mythic}{maxilvl}")
CACHE_OF_ACQUIRED_TREASURES_WAND.event_type = EventType.DAMAGE

#### OTHER ####
# pvp badge
# s.add_spell(spell_type=TYPE_TRINKET, spell_id=345228, cooldown=60,  duration=15, name="Gladiator's Badge", icon="spell_holy_championsbond.jpg", wowhead_data=f"item=185197&bonus=7315:1518:6646")
# Other Trinkets
# s.add_spell(spell_type=TYPE_TRINKET, spell_id=348139, cooldown=90,  duration=9,  name="Instructor's Divine Bell", icon="inv_misc_bell_01.jpg", wowhead_data="item=184842&&bonus=1472:5894:6646")

# tracking the buff it gives. spell would be 367953 with 4min CD
JAILER_MACE     = WowSpell(spell_type=TYPE_TRINKET, spell_id=368696, cooldown=0,  duration=60,  color="#7f4af0", name="Gavel of the First Arbiter", icon="inv_mace_2h_jailerpc_d_01.jpg", wowhead_data=f"item=189862{mythic}&ilvl=285")


########################################################################################################################


# everyone
for s in ALL_SPECS:
    s.add_spells(IQD, ORDNANCE, THE_FIRST_SIGIL)

# Intellect users
for s in INT_SPECS:
    s.add_spells(RUBY, ORB_OF_TORMENT)

# Agility Users
for s in AGI_SPECS:
    s.add_spells(EARTHBREAKERS)
    s.add_buffs(CACHE_OF_ACQUIRED_TREASURES_AXE, CACHE_OF_ACQUIRED_TREASURES_SWORD)
    s.add_events(CACHE_OF_ACQUIRED_TREASURES_WAND)

# Strength Users
for s in STR_SPECS:
    s.add_spells(POWER_CRYSTAL, EARTHBREAKERS)
    s.add_buffs(JAILER_MACE)

for s in [DRUID_FERAL, HUNTER_SURVIVAL, MONK_BREWMASTER, DRUID_GUARDIAN]:
    # 2h Agi on use weapon https://www.wowhead.com/item=186404/jotungeirr-destinys-call?bonus=7757
    s.add_spell(spell_type=TYPE_TRINKET, spell_id=357773, cooldown=180, duration=30, color="#7f4af0", name="Jotungeirr, Destiny's Call", icon="inv_polearm_2h_mawraid_d_01.jpg", wowhead_data=f"item=186404{mythic}&ilvl=252")


# hide all trinkets by default
for spell in WowSpell.all:
    if spell.spell_type == TYPE_TRINKET:
        spell.show = False
