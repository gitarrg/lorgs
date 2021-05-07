#!/usr/bin/env python
"""Script to create all Spells."""

# pylint: disable=line-too-long

# IMPORT THIRD PARTY LIBRARIES
import dotenv
dotenv.load_dotenv() # pylint: disable=wrong-import-position

# IMPORT LOCAL LIBRARIES
from lorgs import db
from lorgs.models.specs import WowClass
from lorgs.models.specs import WowRole
from lorgs.models.specs import WowSpec
from lorgs.models.specs import WowSpell
from lorgs.models.specs import SpecSpells


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
#       Fetch
#
################################################################################

# pylint: disable=C0326

# ROLES
TANK = WowRole.query.filter_by(code="tank").first()
HEAL = WowRole.query.filter_by(code="heal").first()
MDPS = WowRole.query.filter_by(code="mdps").first()
RDPS = WowRole.query.filter_by(code="rdps").first()
ROLES = [TANK, HEAL, MDPS, RDPS]


# CLASSES
WARRIOR     = WowClass.query.get(1)
PALADIN     = WowClass.query.get(2)
HUNTER      = WowClass.query.get(3)
ROGUE       = WowClass.query.get(4)
PRIEST      = WowClass.query.get(5)
DEATHKNIGHT = WowClass.query.get(6)
SHAMAN      = WowClass.query.get(7)
MAGE        = WowClass.query.get(8)
WARLOCK     = WowClass.query.get(9)
MONK        = WowClass.query.get(10)
DRUID       = WowClass.query.get(11)
DEMONHUNTER = WowClass.query.get(12)


# SPECS
WARRIOR_ARMS          = WowSpec.query.get(71)
WARRIOR_FURY          = WowSpec.query.get(72)
WARRIOR_PROT          = WowSpec.query.get(73)
PALADIN_HOLY          = WowSpec.query.get(65)
PALADIN_PROTECTION    = WowSpec.query.get(66)
PALADIN_RETRIBUTION   = WowSpec.query.get(70)
HUNTER_BEASTMASTERY   = WowSpec.query.get(253)
HUNTER_MARKSMANSHIP   = WowSpec.query.get(254)
HUNTER_SURVIVAL       = WowSpec.query.get(255)
ROGUE_ASSASSINATION   = WowSpec.query.get(259)
ROGUE_OUTLAW          = WowSpec.query.get(260)
ROGUE_SUBTLETY        = WowSpec.query.get(261)
PRIEST_DISCIPLINE     = WowSpec.query.get(256)
PRIEST_HOLY           = WowSpec.query.get(257)
PRIEST_SHADOW         = WowSpec.query.get(258)
DEATHKNIGHT_BLOOD     = WowSpec.query.get(250)
DEATHKNIGHT_FROST     = WowSpec.query.get(251)
DEATHKNIGHT_UNHOLY    = WowSpec.query.get(252)
SHAMAN_ELEMENTAL      = WowSpec.query.get(262)
SHAMAN_ENHANCEMENT    = WowSpec.query.get(263)
SHAMAN_RESTORATION    = WowSpec.query.get(264)
MAGE_ARCANE           = WowSpec.query.get(62)
MAGE_FIRE             = WowSpec.query.get(63)
MAGE_FROST            = WowSpec.query.get(64)
WARLOCK_AFFLICTION    = WowSpec.query.get(265)
WARLOCK_DEMONOLOGY    = WowSpec.query.get(266)
WARLOCK_DESTRUCTION   = WowSpec.query.get(267)
MONK_BREWMASTER       = WowSpec.query.get(268)
MONK_MISTWEAVER       = WowSpec.query.get(269)
MONK_WINDWALKER       = WowSpec.query.get(270)
DRUID_BALANCE         = WowSpec.query.get(102)
DRUID_FERAL           = WowSpec.query.get(103)
DRUID_GUARDIAN        = WowSpec.query.get(104)
DRUID_RESTORATION     = WowSpec.query.get(105)
DEMONHUNTER_HAVOC     = WowSpec.query.get(577)
DEMONHUNTER_VENGEANCE = WowSpec.query.get(581)


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

SHAMAN_RESTORATION.add_spell(spell_id=108280, cooldown=180, duration=10) # Healing Tide
SHAMAN_RESTORATION.add_spell(spell_id=98008,  cooldown=180, duration=6, color="#24b385")  # Spirit Link
SHAMAN_RESTORATION.add_spell(spell_id=16191,  cooldown=180, duration=8, show=False, color=COL_MANA)  # Mana Tide
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


################################################################################

db.session.add_all(ROLES)
db.session.commit()


#########################


def set_trinkets_show_false():
    spells = (
        WowSpell.query
        .join(SpecSpells)
        .filter(SpecSpells.group_id >= 1000)
        .all()
    )

    for spell in spells:
        spell.show = False

    db.session.add_all(spells)
    db.session.commit()


set_trinkets_show_false()
db.session.remove()


"""
print("HEY")
for spec in _all_specs:
    for spell in spec.spells:
        spell_group
        print(spell, spell.group, spell.group.role)

# disable all by default
# for spell in WowSpell.all:
#     if spell.group.role == ITEM:
#         spell.show = False
#
"""
