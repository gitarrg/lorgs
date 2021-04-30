
# pylint: disable=line-too-long

from lorgs import utils
from lorgs.models.specs import WowClass
from lorgs.models.specs import WowRole
from lorgs.models.specs import WowSpec
from lorgs.models.specs import WowSpell


################################################################################
#
#   ROLES
#
################################################################################
TANK = WowRole(code="tank", name="Tank", sort_index=10)
HEAL = WowRole(code="heal", name="Healer", sort_index=20)
MDPS = WowRole(code="mdps", name="Melee", sort_index=30)
RDPS = WowRole(code="rdps", name="Range", sort_index=40)
ROLES = [TANK, HEAL, MDPS, RDPS]


################################################################################
#
#   CLASSES AND SPECS
#
################################################################################

#   Warrior
WARRIOR = WowClass(name="Warrior", color="#C69B6D")
WARRIOR_ARMS = WARRIOR.add_spec(name="Arms", role=MDPS)
WARRIOR_FURY = WARRIOR.add_spec(name="Fury", role=MDPS)
WARRIOR_PROT = WARRIOR.add_spec(name="Protection", role=TANK, short_name="Prot")

################################
#   Paladin
PALADIN = WowClass(name="Paladin", color="#F48CBA")
PALADIN_HOLY = PALADIN.add_spec(name="Holy", role=HEAL)
PALADIN_PROTECTION = PALADIN.add_spec(name="Protection", role=TANK, short_name="Prot")
PALADIN_RETRIBUTION = PALADIN.add_spec(name="Retribution", role=MDPS, short_name="Ret")

################################
# Hunter
HUNTER = WowClass(name="Hunter", color="#AAD372")
HUNTER_BEASTMASTERY = HUNTER.add_spec(name="Beast Mastery", role=RDPS)
HUNTER_MARKSMANSHIP = HUNTER.add_spec(name="Marksmanship", role=RDPS)
HUNTER_SURVIVAL = HUNTER.add_spec(name="Survival", role=MDPS)

################################
#   Rouge
ROGUE = WowClass(name="Rogue", color="#FFF468")
ROGUE_ASSASSINATION = ROGUE.add_spec(name="Assassination", role=MDPS, short_name="Assa")
ROGUE_OUTLAW = ROGUE.add_spec(name="Outlaw", role=MDPS)
ROGUE_SUBTLETY = ROGUE.add_spec(name="Subtlety", role=MDPS)

################################
#   Priest
PRIEST = WowClass(name="Priest", color="#FFFFFF")
PRIEST_DISCIPLINE = PRIEST.add_spec(name="Discipline", role=HEAL, short_name="Disc")
PRIEST_HOLY = PRIEST.add_spec(name="Holy", role=HEAL)
PRIEST_SHADOW = PRIEST.add_spec(name="Shadow", role=RDPS)

################################
# DK
DEATHKNIGHT = WowClass(name="Death Knight", color="#C41E3A")
DEATHKNIGHT_BLOOD = DEATHKNIGHT.add_spec(name="Blood", role=TANK)
DEATHKNIGHT_FROST = DEATHKNIGHT.add_spec(name="Frost", role=MDPS)
DEATHKNIGHT_UNHOLY = DEATHKNIGHT.add_spec(name="Unholy", role=MDPS)

################################
#   Shaman
SHAMAN = WowClass(name="Shaman", color="#0070DD")
SHAMAN_ELEMENTAL = SHAMAN.add_spec(name="Elemental", role=RDPS)
SHAMAN_ENHANCEMENT = SHAMAN.add_spec(name="Enhancement", role=MDPS)
SHAMAN_RESTORATION = SHAMAN.add_spec(name="Restoration", role=HEAL, short_name="Resto")

################################
#   Mage
MAGE = WowClass(name="Mage", color="#3FC7EB")
MAGE_ARCANE = MAGE.add_spec(name="Arcane", role=RDPS)
MAGE_FIRE = MAGE.add_spec(name="Fire", role=RDPS)
MAGE_FROST = MAGE.add_spec(name="Frost", role=RDPS)

################################
#   Warlock
WARLOCK = WowClass(name="Warlock", color="#8788EE")
WARLOCK_AFFLICTION = WARLOCK.add_spec(name="Affliction", role=RDPS, short_name="Aff")
WARLOCK_DEMONOLOGY = WARLOCK.add_spec(name="Demonology", role=RDPS, short_name="Demo")
WARLOCK_DESTRUCTION = WARLOCK.add_spec(name="Destruction", role=RDPS)

################################
# Monk
MONK = WowClass(name="Monk", color="#00FF98")
MONK_BREWMASTER = MONK.add_spec(name="Brewmaster", role=TANK)
MONK_MISTWEAVER = MONK.add_spec(name="Mistweaver", role=HEAL)
MONK_WINDWALKER = MONK.add_spec(name="Windwalker", role=MDPS)

################################
# Druid
DRUID = WowClass(name="Druid", color="#FF7C0A")
DRUID_BALANCE = DRUID.add_spec(name="Balance", role=RDPS)
DRUID_FERAL = DRUID.add_spec(name="Feral", role=MDPS)
DRUID_GUARDIAN = DRUID.add_spec(name="Guardian", role=TANK)
DRUID_RESTORATION = DRUID.add_spec(name="Restoration", role=HEAL)

################################
# DH
DEMONHUNTER = WowClass(name="Demon Hunter", color="#A330C9")
DEMONHUNTER_HAVOC = DEMONHUNTER.add_spec(name="Havoc", role=MDPS)
DEMONHUNTER_VENGEANCE = DEMONHUNTER.add_spec(name="Vengeance", role=TANK)

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


# Because the values are constant..  lets just save them here
CLASSES = [
    WARRIOR,
    PALADIN,
    HUNTER,
    ROGUE,
    PRIEST,
    DEATHKNIGHT,
    SHAMAN,
    MAGE,
    WARLOCK,
    MONK,
    DRUID,
    DEMONHUNTER,
]

SPECS = [spec for wow_class in CLASSES for spec in wow_class.specs]


for role in ROLES:
    role.specs = [spec for spec in SPECS if spec.role == role]


################################################################################
#
#   SPELLS
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


################################
#   Warrior
WARRIOR.add_spell(spell_id=325886, cooldown=90, duration=12, color=COL_NIGHTFAE) # Nightfae: Ancient Aftershock
WARRIOR.add_spell(spell_id=97462, cooldown=180, duration=10, show=False) # Rally Cry
WARRIOR_FURY.add_spell(spell_id=1719, cooldown=60, duration=10) # Recklessness # reduced by Anger Management
WARRIOR_FURY.add_spell(spell_id=46924, cooldown=60, duration=4) # Bladestorm


################################
#   Paladin
# paladin.add_spell(spell_id=105809, cooldown=180, duration=20, show=False) # Holy Avenger
PALADIN.add_spell(spell_id=304971, cooldown=CD_1_MIN, show=False, color=COL_KYRIAN) # Covenant: Divine Toll
PALADIN.add_spell(spell_id=316958, cooldown=CD_4_MIN, duration=30, color=COL_VENTYR) # Covenant: Ashen Hallow
PALADIN.add_spell(spell_id=31884, cooldown=CD_2_MIN, duration=20) # Wings
PALADIN_HOLY.add_spell(spell_id=31821, cooldown=CD_3_MIN, duration=8, color="#dc65f5") # Aura Mastery


################################
# Hunter
HUNTER.add_spell(spell_id=328231, cooldown=120, duration=15, color=COL_NIGHTFAE) # Covenant: Wild Spirits
HUNTER_BEASTMASTERY.add_spell(spell_id=193530, cooldown=180, duration=20) # Aspect of the Wild
HUNTER_BEASTMASTERY.add_spell(spell_id=19574, cooldown=30, duration=15, show=False, color="#9c8954") # Bestial Wrath
# hunter_survival.add_spell(spell_id=266779, cooldown=120, duration=20) # Coordinated Assault
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
# shaman.add_spell(spell_id=326059, cooldown=45, show=False, color=COL_NECROLORD)  # Necro: Primordial Wave
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
#   POTIONS & TRINKETS
#
################################################################################

ITEM = WowRole(code="z_item", name="Items")
OTHER = WowClass(name="Other", color="#cccccc")

OTHER_POTION = OTHER.add_spec(name="Potions", role=ITEM)
OTHER_TRINKET = OTHER.add_spec(name="Trinkets", role=ITEM)


_specs_dps = MDPS.specs+RDPS.specs

_specs_int = HEAL.specs + [PRIEST_SHADOW, SHAMAN_ELEMENTAL, MAGE, WARLOCK, DRUID_BALANCE]
_specs_agi = [HUNTER, ROGUE, SHAMAN_ENHANCEMENT, MONK_WINDWALKER, DRUID_FERAL, DEMONHUNTER]
_specs_str = [WARRIOR, PALADIN_RETRIBUTION, DEATHKNIGHT]

for spec in HEAL.specs:
    spec.add_spell(group=OTHER_POTION, spell_id=307161, cooldown=300, duration=10, show=False, color=COL_MANA) # Mana Channel Pot
    spec.add_spell(group=OTHER_POTION, spell_id=307193, cooldown=300, show=False, color=COL_MANA)              # Mana Pot
    spec.add_spell(group=OTHER_POTION, spell_id=307495, cooldown=300, duration=25, show=False, color=_COLOR_POT_EXTRA) # Phantom Fire

for spec in MDPS.specs+RDPS.specs:
    spec.add_spell(group=OTHER_POTION, spell_id=307495, cooldown=300, duration=25, show=False, color=_COLOR_POT_EXTRA) # Phantom Fire

for spec in _specs_int:
    spec.add_spell(group=OTHER_POTION, spell_id=307162, cooldown=300, duration=25, show=False, color=_COLOR_POT_MAINSTAT) # Intellect Pot

for spec in _specs_agi:
    spec.add_spell(group=OTHER_POTION, spell_id=307159, cooldown=300, duration=25, show=False, color=_COLOR_POT_MAINSTAT) # Agility Pot

for spec in _specs_str:
    spec.add_spell(group=OTHER_POTION, spell_id=307164, cooldown=300, duration=25, show=False, color=_COLOR_POT_MAINSTAT) # Strength Pot


################################################################################
#
#   TRINKETS (and all class-potions)
#
################################################################################

# everyone
for spec in WowSpec.all:

    spec.add_spell(group=OTHER_POTION, spell_id=6262, wowhead_data="item=5512") # Healthstone
    spec.add_spell(group=OTHER_POTION, spell_id=307192, cooldown=CD_5_MIN, color="#e35f5f", wowhead_data="item=171267") # Healthpot

    # Raid Trinkets
    spec.add_spell(group=OTHER_TRINKET, spell_id=345019, cooldown=90) # Skulking Predator

    spec.add_spell(group=OTHER_TRINKET, spell_id=349857, cooldown=90, wowhead_data="item=184030&bonus=7359:6646")              # Dreadfire Vessel
    spec.add_spell(group=OTHER_TRINKET, spell_id=330323, cooldown=180, wowhead_data="item=179350&ilvl=226")                    # Quantum Device
    spec.add_spell(group=OTHER_TRINKET, spell_id=345539, cooldown=180, duration=35, wowhead_data="item=180117&ilvl=226")       # Ordnance (estimated duration)
    spec.add_spell(group=OTHER_TRINKET, spell_id=348139, cooldown=90, duration=9, wowhead_data="item=184842&ilvl=226")         # Divine Bell

for spec in _specs_int:
    spec.add_spell(group=OTHER_TRINKET, spell_id=345801, cooldown=120, duration=15, wowhead_data="item=178809&ilvl=226")  # Soulletting Ruby
    spec.add_spell(group=OTHER_TRINKET, spell_id=345251, cooldown=60, duration=15, wowhead_data="item=184019&bonus=7359:6646") # Soul Igniter


for spec in _specs_agi:
    spec.add_spell(group=OTHER_TRINKET, spell_id=345530, cooldown=90, duration=6, wowhead_data="item=180116&bonus=7359:6646")  # Overcharged Anima Battery
    spec.add_spell(group=OTHER_TRINKET, spell_id=345251, cooldown=60, duration=15, wowhead_data="item=184025&ilvl=226")        # Memory of Past Sins


for spec in _specs_str:

    # Other Trinkets
    item = spec.add_spell(group=OTHER_TRINKET, spell_id=345228, cooldown=CD_1_MIN, duration=15) # Badge


# disable all by default
for spell in WowSpell.all:
    if spell.group.role == ITEM:
        spell.show = False


# load spell icons
SPELLS = utils.uniqify(WowSpell.all, key=lambda spell: spell.spell_id)
