#!/usr/bin/env python
"""Models for Raids and RaidBosses."""
# IMPORT STANDARD LIBRARIES
import json
import aiofiles
import asyncio

# pylint: disable=line-too-long
# pylint: disable=C0326  # spaces

# IMPORT LOCAL LIBRARIES
# from lorgs import db
from lorgs.models.specs import WowClass
from lorgs.models.specs import WowRole
from lorgs.models.specs import WowSpec
from lorgs.models.specs import WowSpell


################################################################################
#
#   ROLES
#
################################################################################
TANK = WowRole(code="tank", name="Tank")
HEAL = WowRole(code="heal", name="Healer")
MDPS = WowRole(code="mdps", name="Melee")
RDPS = WowRole(code="rdps", name="Range")
ROLES = [TANK, HEAL, MDPS, RDPS]

################################################################################
#
#   CLASSES
#
WARRIOR      = WowClass(id=1,  name="Warrior",       color="#C69B6D")
PALADIN      = WowClass(id=2,  name="Paladin",       color="#F48CBA")
HUNTER       = WowClass(id=3,  name="Hunter",        color="#AAD372")
ROGUE        = WowClass(id=4,  name="Rogue",         color="#FFF468")
PRIEST       = WowClass(id=5,  name="Priest",        color="#FFFFFF")
DEATHKNIGHT  = WowClass(id=6,  name="Death Knight",  color="#C41E3A")
SHAMAN       = WowClass(id=7,  name="Shaman",        color="#0070DD")
MAGE         = WowClass(id=8,  name="Mage",          color="#3FC7EB")
WARLOCK      = WowClass(id=9,  name="Warlock",       color="#8788EE")
MONK         = WowClass(id=10, name="Monk",          color="#00FF98")
DRUID        = WowClass(id=11, name="Druid",         color="#FF7C0A")
DEMONHUNTER  = WowClass(id=12, name="Demon Hunter",  color="#A330C9")

################################################################################
#
#   SPECS
#

WARRIOR_ARMS          = WowSpec(id=71,  role=MDPS, wow_class=WARRIOR,      name="Arms")
WARRIOR_FURY          = WowSpec(id=72,  role=MDPS, wow_class=WARRIOR,      name="Fury")
WARRIOR_PROT          = WowSpec(id=73,  role=TANK, wow_class=WARRIOR,      name="Protection")
PALADIN_HOLY          = WowSpec(id=65,  role=HEAL, wow_class=PALADIN,      name="Holy")
PALADIN_PROTECTION    = WowSpec(id=66,  role=TANK, wow_class=PALADIN,      name="Protection")
PALADIN_RETRIBUTION   = WowSpec(id=70,  role=MDPS, wow_class=PALADIN,      name="Retribution")
HUNTER_BEASTMASTERY   = WowSpec(id=253, role=RDPS, wow_class=HUNTER,       name="Beastmastery")
HUNTER_MARKSMANSHIP   = WowSpec(id=254, role=RDPS, wow_class=HUNTER,       name="Marksmanship")
HUNTER_SURVIVAL       = WowSpec(id=255, role=MDPS, wow_class=HUNTER,       name="Survival")
ROGUE_ASSASSINATION   = WowSpec(id=259, role=MDPS, wow_class=ROGUE,        name="Assassination")
ROGUE_OUTLAW          = WowSpec(id=260, role=MDPS, wow_class=ROGUE,        name="Outlaw")
ROGUE_SUBTLETY        = WowSpec(id=261, role=MDPS, wow_class=ROGUE,        name="Subtlety")
PRIEST_DISCIPLINE     = WowSpec(id=256, role=HEAL, wow_class=PRIEST,       name="Discipline")
PRIEST_HOLY           = WowSpec(id=257, role=HEAL, wow_class=PRIEST,       name="Holy")
PRIEST_SHADOW         = WowSpec(id=258, role=RDPS, wow_class=PRIEST,       name="Shadow")
DEATHKNIGHT_BLOOD     = WowSpec(id=250, role=TANK, wow_class=DEATHKNIGHT,  name="Blood")
DEATHKNIGHT_FROST     = WowSpec(id=251, role=MDPS, wow_class=DEATHKNIGHT,  name="Frost")
DEATHKNIGHT_UNHOLY    = WowSpec(id=252, role=MDPS, wow_class=DEATHKNIGHT,  name="Unholy")
SHAMAN_ELEMENTAL      = WowSpec(id=262, role=RDPS, wow_class=SHAMAN,       name="Elemental")
SHAMAN_ENHANCEMENT    = WowSpec(id=263, role=MDPS, wow_class=SHAMAN,       name="Enhancement")
SHAMAN_RESTORATION    = WowSpec(id=264, role=HEAL, wow_class=SHAMAN,       name="Restoration")
MAGE_ARCANE           = WowSpec(id=62,  role=RDPS, wow_class=MAGE,         name="Arcane")
MAGE_FIRE             = WowSpec(id=63,  role=RDPS, wow_class=MAGE,         name="Fire")
MAGE_FROST            = WowSpec(id=64,  role=RDPS, wow_class=MAGE,         name="Frost")
WARLOCK_AFFLICTION    = WowSpec(id=265, role=RDPS, wow_class=WARLOCK,      name="Affliction")
WARLOCK_DEMONOLOGY    = WowSpec(id=266, role=RDPS, wow_class=WARLOCK,      name="Demonology")
WARLOCK_DESTRUCTION   = WowSpec(id=267, role=RDPS, wow_class=WARLOCK,      name="Destruction")
MONK_BREWMASTER       = WowSpec(id=268, role=TANK, wow_class=MONK,         name="Brewmaster")
MONK_MISTWEAVER       = WowSpec(id=269, role=HEAL, wow_class=MONK,         name="Mistweaver")
MONK_WINDWALKER       = WowSpec(id=270, role=MDPS, wow_class=MONK,         name="Windwalker")
DRUID_BALANCE         = WowSpec(id=102, role=RDPS, wow_class=DRUID,        name="Balance")
DRUID_FERAL           = WowSpec(id=103, role=MDPS, wow_class=DRUID,        name="Feral")
DRUID_GUARDIAN        = WowSpec(id=104, role=TANK, wow_class=DRUID,        name="Guardian")
DRUID_RESTORATION     = WowSpec(id=105, role=HEAL, wow_class=DRUID,        name="Restoration")
DEMONHUNTER_HAVOC     = WowSpec(id=577, role=MDPS, wow_class=DEMONHUNTER,  name="Havoc")
DEMONHUNTER_VENGEANCE = WowSpec(id=581, role=TANK, wow_class=DEMONHUNTER,  name="Vengeance")


for spec in WowSpec.all:
    spec.role.specs.append(spec)


WARRIOR_PROT.short_name        = "Prot"
PALADIN_PROTECTION.short_name  = "Prot"
PALADIN_RETRIBUTION.short_name = "Ret"
ROGUE_ASSASSINATION.short_name = "Assa"
PRIEST_DISCIPLINE.short_name   = "Disc"
SHAMAN_RESTORATION.short_name  = "Resto"
WARLOCK_AFFLICTION.short_name  = "Aff"
WARLOCK_DEMONOLOGY.short_name  = "Demo"

# sorry guys...
WARRIOR_PROT.supported = False
PALADIN_PROTECTION.supported = False
DEATHKNIGHT_BLOOD.supported = False
MONK_BREWMASTER.supported = False
DRUID_GUARDIAN.supported = False
DEMONHUNTER_VENGEANCE.supported = False

# mdps
WARRIOR_ARMS.supported = False
HUNTER_SURVIVAL.supported = False
ROGUE_ASSASSINATION.supported = False
ROGUE_SUBTLETY.supported = False
ROGUE_OUTLAW.supported = False
DEATHKNIGHT_FROST.supported = False
DRUID_FERAL.supported = False

# rdps
PRIEST_SHADOW.supported = False
MAGE_ARCANE.supported = False
MAGE_FROST.supported = False


################################################################################
#
#   OTHER
# its a bit of a hack.. but works for now
# all ids start at 1000 here, to help separate them later.
#
################################################################################

ROLE_ITEM     = WowRole(code="item", name="Items")
OTHER         = WowClass(id=1001, name="Other", color="#cccccc")
OTHER_POTION  = WowSpec(id=1001, role=ROLE_ITEM, wow_class=OTHER,  name="Potions")
OTHER_TRINKET = WowSpec(id=1002, role=ROLE_ITEM, wow_class=OTHER,  name="Trinkets")


################################################################################
#
#   CONSTANTS
#
################################################################################

CD_1_MIN = 1 * 60 # 60
CD_2_MIN = 2 * 60 # 120
CD_3_MIN = 3 * 60 # 180
CD_4_MIN = 4 * 60 # 240
CD_5_MIN = 5 * 60 # 300

# Some Colors
COL_NIGHTFAE = "#8d5ca1"
COL_VENTYR = "FireBrick"
COL_KYRIAN = "LightSkyBlue"
COL_NECROLORD = "MediumSeaGreen"

COL_MANA = "#5397ed"

_COLOR_MANA = COL_MANA
_COLOR_POT_MAINSTAT = "#b576e8"
_COLOR_POT_EXTRA = "#57bd8b"


################################################################################
#
#       SPELLS: CLASSES / SPECS
#
################################################################################

################################
#   Warrior
WARRIOR.add_spell(spell_id=325886, cooldown=90, duration=12, color=COL_NIGHTFAE) # Nightfae: Ancient Aftershock
WARRIOR.add_spell(spell_id=97462, cooldown=180, duration=10, show=False) # Rally Cry
WARRIOR_FURY.add_spell(spell_id=1719, cooldown=60, duration=10) # Recklessness # reduced by Anger Management
WARRIOR_FURY.add_spell(spell_id=46924, cooldown=60, duration=4) # Bladestorm

################################
#   Paladin
# PALADIN.add_spell(spell_id=105809, cooldown=180, duration=20, show=False) # Holy Avenger
PALADIN.add_spell(spell_id=304971, cooldown=CD_1_MIN, show=False, color=COL_KYRIAN) # Covenant: Divine Toll
PALADIN.add_spell(spell_id=316958, cooldown=CD_4_MIN, duration=30, color=COL_VENTYR) # Covenant: Ashen Hallow
PALADIN.add_spell(spell_id=31884, cooldown=CD_2_MIN, duration=20) # Wings
PALADIN_HOLY.add_spell(spell_id=31821, cooldown=CD_3_MIN, duration=8, color="#dc65f5") # Aura Mastery

################################
# Hunter
HUNTER.add_spell(spell_id=328231, cooldown=120, duration=15, color=COL_NIGHTFAE) # Covenant: Wild Spirits
HUNTER_BEASTMASTERY.add_spell(spell_id=193530, cooldown=180, duration=20) # Aspect of the Wild
HUNTER_BEASTMASTERY.add_spell(spell_id=19574, cooldown=30, duration=15, show=False, color="#9c8954") # Bestial Wrath
# HUNTER_SURVIVAL.add_spell(spell_id=266779, cooldown=120, duration=20) # Coordinated Assault
HUNTER_MARKSMANSHIP.add_spell(spell_id=288613, cooldown=120, duration=15, show=False) # Trueshot

################################
#   Rouge

################################
#   Priest
PRIEST.add_spell(spell_id=10060, cooldown=CD_2_MIN, duration=20, show=False, color="#1fbcd1") # Power Infusion
# PRIEST_SHADOW.add_spell(spell_id=34433, cooldown=180, duration=15) # Shadowfiend
# PRIEST_SHADOW.add_spell(spell_id=228260, cooldown=90) # Void Erruption
# PRIEST_DISCIPLINE.add_spell(spell_id=34433, cooldown=180, duration=15, show=False) # Shadowfiend
#TODO: add mindbender?
PRIEST_DISCIPLINE.add_spell(spell_id=62618,  cooldown=180, duration=10, color="#b3ad91")  #Power Word: Cuddle
PRIEST_DISCIPLINE.add_spell(spell_id=109964,  cooldown=60, duration=10, color="#d7abdb")  # Spirit Shell
PRIEST_DISCIPLINE.add_spell(spell_id=47536,  cooldown=90, duration=8, show=False)  # Rapture
PRIEST_DISCIPLINE.add_spell(spell_id=246287,  cooldown=90, show=False)  # Evengelism
PRIEST_HOLY.add_spell(spell_id=64843, cooldown=180, duration=8, color="#d7abdb") # Hymn
PRIEST_HOLY.add_spell(spell_id=265202, cooldown=240) # Savl (not showing CD, because dynamic)
PRIEST_HOLY.add_spell(spell_id=200183, cooldown=120, duration=20, show=False) # Apotheosis

################################
# DK
DEATHKNIGHT.add_spell(spell_id=51052, cooldown=120, duration=10, show=False)  # Anti-Magic Zone
DEATHKNIGHT_UNHOLY.add_spell(spell_id=42650, cooldown=4*60, duration=30)  # Army (usually 4min with talent)
DEATHKNIGHT_UNHOLY.add_spell(spell_id=275699, cooldown=60, duration=15, show=False)  # Apocalypse (90sec -> 60sec talent)

################################
#   Shaman
# SHAMAN.add_spell(spell_id=326059, cooldown=45, show=False, color=COL_NECROLORD)  # Necro: Primordial Wave
SHAMAN.add_spell(spell_id=320674, cooldown=90, show=False, color=COL_VENTYR)  # Ventyr: Chain Harvest
SHAMAN_ELEMENTAL.add_spell(spell_id=191634, cooldown=60, show=True, color="DeepSkyBlue")  # Stormkeeper
SHAMAN_ELEMENTAL.add_spell(spell_id=198067, cooldown=150, show=True, color="DarkOrange")  # Fire Elemental

SHAMAN_ENHANCEMENT.add_spell(spell_id=114051, cooldown=CD_3_MIN, show=True)  # Ascendance
SHAMAN_ENHANCEMENT.add_spell(spell_id=51533, cooldown=CD_2_MIN, show=True)  # Feral Spirit

SHAMAN_RESTORATION.add_spell(spell_id=108280,  cooldown=180, duration=10) # Healing Tide
SHAMAN_RESTORATION.add_spell(spell_id=98008,   cooldown=180, duration=6, color="#24b385")  # Spirit Link
SHAMAN_RESTORATION.add_spell(spell_id=16191,   cooldown=180, duration=8, show=False, color=COL_MANA)  # Mana Tide
SHAMAN_RESTORATION.add_spell(spell_id=207399,  cooldown=300, duration=30, color="#d15a5a")  # Ahnk totem
SHAMAN_RESTORATION.add_spell(spell_id=114052,  cooldown=180, duration=15)  # Ascendance

################################
#   Mage
MAGE.add_spell(spell_id=314791, cooldown=60, duration=3.1, show=False, color=COL_NIGHTFAE) # Shifting Power
MAGE_FIRE.add_spell(spell_id=190319, cooldown=60, duration=10, color="#e3b02d") # Combustion
MAGE_FIRE.add_spell(spell_id=153561, cooldown=45, show=False) # Meteor

################################
#   Warlock
WARLOCK.add_spell(spell_id=325640, cooldown=60, duration=8, show=False, color=COL_NIGHTFAE) # Soulrot
WARLOCK_AFFLICTION.add_spell(spell_id=205180, cooldown=180, duration=8, color="#49ad6e") # Darkglare
WARLOCK_AFFLICTION.add_spell(spell_id=113860, cooldown=120, duration=20, color="#c35ec4") # Dark Soul: Misery
WARLOCK_AFFLICTION.add_spell(spell_id=205179, cooldown=45, duration=16, color="#7833b0") # PS
WARLOCK_DEMONOLOGY.add_spell(spell_id=265187, cooldown=90, duration=15, color="#9150ad") # Tyrant
WARLOCK_DEMONOLOGY.add_spell(spell_id=111898, cooldown=120, duration=17, color="#c46837") # Felguard
WARLOCK_DEMONOLOGY.add_spell(spell_id=267217, cooldown=180, duration=15) # Netherportal
WARLOCK_DESTRUCTION.add_spell(spell_id=1122, cooldown=180, duration=30, color="#91c45a") # Infernal
WARLOCK_DESTRUCTION.add_spell(spell_id=113858, cooldown=120, duration=20, color="#c35ec4") # Dark Soul: Instability

################################
# Monk
MONK.add_spell(spell_id=322109, cooldown=180, color="#c72649") # Touch of Death
MONK.add_spell(spell_id=115203, cooldown=360, duration=15, show=False) # Fort Brew
MONK.add_spell(spell_id=310454, cooldown=120, duration=30, show=False, color=COL_KYRIAN) # Weapons of Order
MONK_MISTWEAVER.add_spell(spell_id=322118, cooldown=180, duration=3.5) # Yulon
MONK_MISTWEAVER.add_spell(spell_id=115310, cooldown=180, color="#00FF98") # Revival
MONK_MISTWEAVER.add_spell(spell_id=325197, cooldown=180, duration=25, color="#e0bb36") # Chiji
MONK_WINDWALKER.add_spell(spell_id=123904, cooldown=120, duration=24, color="#8cdbbc") # Xuen
MONK_WINDWALKER.add_spell(spell_id=137639, cooldown=90, duration=15, color="#be53db") # Storm, Earth and Fire

################################
# Druid
DRUID.add_spell(spell_id=323764, cooldown=120, duration=4, show=False, color=COL_NIGHTFAE)  # Convoke
DRUID_RESTORATION.add_spell(spell_id=197721, cooldown=90, duration=8, show=False, color="#7ec44d") # Flourish
DRUID_RESTORATION.add_spell(spell_id=29166, cooldown=180, duration=10, show=False, color="#3b97ed") # Innervate
DRUID_RESTORATION.add_spell(spell_id=740, cooldown=180, duration=6, color="#6cbfd9") # Tranquility
DRUID_RESTORATION.add_spell(spell_id=33891, cooldown=180, duration=30) # Tree of Life

# TODO:
# const CUSTOM_IMAGES = {}
# CUSTOM_IMAGES[740] = "/static/images/spells/spell_nature_tranquility.jpg";
DRUID_BALANCE.add_spell(spell_id=194223, cooldown=180, duration=20) # Celestrial
DRUID_BALANCE.add_spell(spell_id=102560, cooldown=180, duration=30) # Incarnation
DRUID_BALANCE.add_spell(spell_id=205636, cooldown=60, duration=10, show=False) # Treants
DRUID_BALANCE.add_spell(spell_id=202770, cooldown=60, duration=8, show=False) # Fury of Elune

################################
# DH
DEMONHUNTER.add_spell(spell_id=306830, cooldown=60, color=COL_KYRIAN) # Elysian Decree
DEMONHUNTER.add_spell(spell_id=323639, cooldown=90, duration=6, color=COL_NIGHTFAE) # The Hunt
DEMONHUNTER.add_spell(spell_id=317009, cooldown=60, color=COL_VENTYR) # Sinful Brand
DEMONHUNTER_HAVOC.add_spell(spell_id=200166, cooldown=CD_4_MIN, duration=30, color="#348540", icon_name="ability_demonhunter_metamorphasisdps.jpg") # Meta
DEMONHUNTER_HAVOC.add_spell(spell_id=196718, cooldown=180, duration=8, show=False) # Darkness
DEMONHUNTER_HAVOC.add_spell(spell_id=196555, cooldown=180, duration=5, show=False) # Netherwalk


################################################################################
#
#       POTIONS & TRINKETS
#
################################################################################

"""
# grab the roles, so we use them to assign trinkets and pots
ITEM_POTION = WowSpec.query.filter_by(name="Potions").first()
ITEM_TRINKET = WowSpec.query.filter_by(name="Trinkets").first()


_specs_dps = MDPS.specs + RDPS.specs
_specs_int = HEAL.specs + [PRIEST_SHADOW, SHAMAN_ELEMENTAL, MAGE, WARLOCK, DRUID_BALANCE]
_specs_agi = [HUNTER, ROGUE, SHAMAN_ENHANCEMENT, MONK_WINDWALKER, DRUID_FERAL, DEMONHUNTER]
_specs_str = [WARRIOR, PALADIN_RETRIBUTION, DEATHKNIGHT]
_all_specs = TANK.specs + HEAL.specs + MDPS.specs + RDPS.specs


for spec in HEAL.specs:
    spec.add_spell(group=ITEM_POTION, spell_id=307161, cooldown=300, duration=10, show=False, color=COL_MANA)          # Mana Channel Pot
    spec.add_spell(group=ITEM_POTION, spell_id=307193, cooldown=300, show=False, color=COL_MANA)                       # Mana Pot
    spec.add_spell(group=ITEM_POTION, spell_id=307495, cooldown=300, duration=25, show=False, color=_COLOR_POT_EXTRA)  # Phantom Fire

for spec in MDPS.specs+RDPS.specs:
    spec.add_spell(group=ITEM_POTION, spell_id=307495, cooldown=300, duration=25, show=False, color=_COLOR_POT_EXTRA) # Phantom Fire

for spec in _specs_int:
    spec.add_spell(group=ITEM_POTION, spell_id=307162, cooldown=300, duration=25, show=False, color=_COLOR_POT_MAINSTAT) # Intellect Pot

for spec in _specs_agi:
    spec.add_spell(group=ITEM_POTION, spell_id=307159, cooldown=300, duration=25, show=False, color=_COLOR_POT_MAINSTAT) # Agility Pot

for spec in _specs_str:
    spec.add_spell(group=ITEM_POTION, spell_id=307164, cooldown=300, duration=25, show=False, color=_COLOR_POT_MAINSTAT) # Strength Pot


################################################################################
#
#       TRINKETS (and all class-potions)
#
################################################################################

# everyone
for spec in _all_specs:

    spec.add_spell(group=ITEM_POTION, spell_id=6262, wowhead_data="item=5512") # Healthstone
    spec.add_spell(group=ITEM_POTION, spell_id=307192, cooldown=CD_5_MIN, color="#e35f5f", wowhead_data="item=171267") # Healthpot

    # Raid Trinkets
    spec.add_spell(group=ITEM_TRINKET, spell_id=345019, cooldown=90) # Skulking Predator
    spec.add_spell(group=ITEM_TRINKET, spell_id=349857, cooldown=90, wowhead_data="item=184030&bonus=7359:6646", spell_name="Dreadfire Vessel") # Dreadfire Vessel

    # Dungeon
    spec.add_spell(group=ITEM_TRINKET, spell_id=330323, cooldown=180, wowhead_data="item=179350&ilvl=226")                    # Quantum Device
    spec.add_spell(group=ITEM_TRINKET, spell_id=345539, cooldown=180, duration=35, wowhead_data="item=180117&ilvl=226")       # Ordnance (estimated duration)
    spec.add_spell(group=ITEM_TRINKET, spell_id=348139, cooldown=90, duration=9, wowhead_data="item=184842&ilvl=226")         # Divine Bell

    # Other Trinkets
    item = spec.add_spell(group=ITEM_TRINKET, spell_id=345228, cooldown=CD_1_MIN, duration=15) # Badge


for spec in _specs_int:
    spec.add_spell(group=ITEM_TRINKET, spell_id=345801, cooldown=120, duration=15, wowhead_data="item=178809&ilvl=226")       # Soulletting Ruby
    spec.add_spell(group=ITEM_TRINKET, spell_id=345251, cooldown=60, duration=15, wowhead_data="item=184019&bonus=7359:6646") # Soul Igniter


for spec in _specs_agi:
    spec.add_spell(group=ITEM_TRINKET, spell_id=345530, cooldown=90, duration=6, wowhead_data="item=180116&bonus=7359:6646")  # Overcharged Anima Battery
    spec.add_spell(group=ITEM_TRINKET, spell_id=345251, cooldown=60, duration=15, wowhead_data="item=184025&ilvl=226")        # Memory of Past Sins

for spec in _specs_str:
    pass
"""

import os
import sys

filename = os.path.dirname(__file__) + "/spell_data.json"

# TODO: find a better place for this
async def load_spell_icons():
    async with aiofiles.open(filename, "r") as f:
        content = await f.read()
        SPELL_INFO = json.loads(content)

    for spell in WowSpell.all:
        spell_info = SPELL_INFO.get(str(spell.spell_id), {})
        spell.spell_name = spell.spell_name or spell_info.get("name")
        spell.icon_name = spell.icon_name or spell_info.get("icon")


asyncio.run(load_spell_icons())
