


from wowtimeline import models as m


# ROLES
TANK = "tank"
HEAL = "heal"
MDPS = "mdps"
RDPS = "rdps"


################################################################################

ENCOUNTERS = [
    {"id": 2398, "name": "Shriekwing", "name_slug": "shriekwing"},
    {"id": 2418, "name": "Huntsman Altimor", "name_slug": "huntsman-altimor"},
    {"id": 2383, "name": "Hungering Destroyer", "name_slug": "hungering-destroyer"},
    {"id": 2402, "name": "Sun King's Salvation", "name_slug": "sun-kings-salvation"},
    {"id": 2405, "name": "Artificer Xy'mox", "name_slug": "artificer-xymox"},
    {"id": 2406, "name": "Lady Inerva Darkvein", "name_slug": "lady-inerva-darkvein"},
    {"id": 2412, "name": "The Council of Blood", "name_slug": "the-council-of-blood"},
    {"id": 2399, "name": "Sludgefist", "name_slug": "sludgefist"},
    {"id": 2417, "name": "Stone Legion Generals", "name_slug": "stone-legion-generals"},
    {"id": 2407, "name": "Sire Denathrius", "name_slug": "sire-denathrius"},
]




################################################################################

# Define all classes and specs

WARRIOR = m.WoWClass(name="Warrior")
WARRIOR_ARMS = WARRIOR.add_spec(name="Arms", role=MDPS)
WARRIOR_FURY = WARRIOR.add_spec(name="Fury", role=MDPS)
WARRIOR_PROTECTION = WARRIOR.add_spec(name="Protection", role=TANK)

PALADIN = m.WoWClass(name="Paladin")
PALADIN_HOLY = PALADIN.add_spec(name="Holy", role=HEAL)
PALADIN_PROTECTION = PALADIN.add_spec(name="Protection", role=TANK)
PALADIN_RETRIBUTION = PALADIN.add_spec(name="Retribution", role=MDPS)

HUNTER = m.WoWClass(name="Hunter")
HUNTER_BEASTMASTERY = HUNTER.add_spec(name="Beast Mastery", role=RDPS)
HUNTER_MARKSMANSHIP = HUNTER.add_spec(name="Marksmanship", role=RDPS)
HUNTER_SURVIVAL = HUNTER.add_spec(name="Survival", role=MDPS)

ROGUE = m.WoWClass(name="Rogue")
ROGUE_ASSASSINATION = ROGUE.add_spec(name="Assassination", role=MDPS)
ROGUE_SUBTLETY = ROGUE.add_spec(name="Subtlety", role=MDPS)
ROGUE_OUTLAW = ROGUE.add_spec(name="Outlaw", role=MDPS)

PRIEST = m.WoWClass(name="Priest")
PRIEST_DISCIPLINE = PRIEST.add_spec(name="Discipline", role=HEAL)
PRIEST_HOLY = PRIEST.add_spec(name="Holy", role=HEAL)
PRIEST_SHADOW = PRIEST.add_spec(name="Shadow", role=RDPS)

DEATHKNIGHT = m.WoWClass(name="Death Knight")
DEATHKNIGHT_BLOOD = DEATHKNIGHT.add_spec(name="Blood", role=TANK)
DEATHKNIGHT_FROST = DEATHKNIGHT.add_spec(name="Frost", role=MDPS)
DEATHKNIGHT_UNHOLY = DEATHKNIGHT.add_spec(name="Unholy", role=MDPS)

SHAMAN = m.WoWClass(name="Shaman")
SHAMAN_ELEMENTAL = SHAMAN.add_spec(name="Elemental", role=RDPS)
SHAMAN_ENHANCEMENT = SHAMAN.add_spec(name="Enhancement", role=MDPS)
SHAMAN_RESTORATION = SHAMAN.add_spec(name="Restoration", role=HEAL)

MAGE = m.WoWClass(name="Mage")
MAGE_ARCANE = MAGE.add_spec(name="Arcane", role=RDPS)
MAGE_FIRE = MAGE.add_spec(name="Fire", role=RDPS)
MAGE_FROST = MAGE.add_spec(name="Frost", role=RDPS)

WARLOCK = m.WoWClass(name="Warlock")
WARLOCK_AFFLICTION = WARLOCK.add_spec(name="Affliction", role=RDPS)
WARLOCK_DEMONOLOGY = WARLOCK.add_spec(name="Demonology", role=RDPS)
WARLOCK_DESTRUCTION = WARLOCK.add_spec(name="Destruction", role=RDPS)

MONK = m.WoWClass(name="Monk")
MONK_BREWMASTER = MONK.add_spec(name="Brewmaster", role=TANK)
MONK_MISTWEAVER = MONK.add_spec(name="Mistweaver", role=HEAL)
MONK_WINDWALKER = MONK.add_spec(name="Windwalker", role=MDPS)

DRUID = m.WoWClass(name="Druid")
DRUID_BALANCE = DRUID.add_spec(name="Balance", role=RDPS)
DRUID_FERAL = DRUID.add_spec(name="Feral", role=MDPS)
DRUID_GUARDIAN = DRUID.add_spec(name="Guardian", role=TANK)
DRUID_RESTORATION = DRUID.add_spec(name="Restoration", role=HEAL)

DEMONHUNTER = m.WoWClass(name="Demon Hunter")
DEMONHUNTER_HAVOC = DEMONHUNTER.add_spec(name="Havoc", role=MDPS)
DEMONHUNTER_VENGEANCE = DEMONHUNTER.add_spec(name="Vengeance", role=TANK)


# sorry guys...
WARRIOR_ARMS.supported = False
WARRIOR_FURY.supported = False
WARRIOR_PROTECTION.supported = False
# PALADIN_HOLY.supported = False
PALADIN_PROTECTION.supported = False
# PALADIN_RETRIBUTION.supported = False
# HUNTER_BEASTMASTERY.supported = False
# HUNTER_MARKSMANSHIP.supported = False
HUNTER_SURVIVAL.supported = False
ROGUE_ASSASSINATION.supported = False
ROGUE_SUBTLETY.supported = False
ROGUE_OUTLAW.supported = False
# PRIEST_DISCIPLINE.supported = False
# PRIEST_HOLY.supported = False
PRIEST_SHADOW.supported = False
DEATHKNIGHT_BLOOD.supported = False
DEATHKNIGHT_FROST.supported = False
# DEATHKNIGHT_UNHOLY.supported = False
SHAMAN_ELEMENTAL.supported = False
SHAMAN_ENHANCEMENT.supported = False
# SHAMAN_RESTORATION.supported = False
MAGE_ARCANE.supported = False
# MAGE_FIRE.supported = False
MAGE_FROST.supported = False
# WARLOCK_AFFLICTION.supported = False
# WARLOCK_DEMONOLOGY.supported = False
# WARLOCK_DESTRUCTION.supported = False
MONK_BREWMASTER.supported = False
# MONK_MISTWEAVER.supported = False
MONK_WINDWALKER.supported = False
# DRUID_BALANCE.supported = False
DRUID_FERAL.supported = False
DRUID_GUARDIAN.supported = False
# DRUID_RESTORATION.supported = False
# DEMONHUNTER_HAVOC.supported = False
DEMONHUNTER_VENGEANCE.supported = False


################################################################################
# Alias to some full lists
#
#
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
    DEMONHUNTER
]

SPECS = [spec for wow_class in CLASSES for spec in wow_class.specs]
SPECS_SUPPORTED = [spec for spec in SPECS if spec.supported]


TANKS = [spec for spec in SPECS if spec.role == TANK]
HEALS = [spec for spec in SPECS if spec.role == HEAL]
MELEE = [spec for spec in SPECS if spec.role == MDPS]
RANGE = [spec for spec in SPECS if spec.role == RDPS]



################################################################################
# Define all the spells we care about
#

# DPS CDs
# WARRIOR.add_spell(spell_id=97462, cooldown=180, duration=10) # Rally Cry
# WARRIOR.add_spell(spell_id=107574, cooldown=90, duration=20) # Avatar
# WARRIOR.add_spell(spell_id=1719, cooldown=90, duration=10) # Recklessness

# PALADIN.add_spell(spell_id=105809, cooldown=180, duration=20, show=False) # Holy Avenger
PALADIN.add_spell(spell_id=304971, cooldown=60, show=False) # Covenant: Divine Toll
PALADIN.add_spell(spell_id=316958, cooldown=240, duration=30) # Covenant: Ashen Hallow
PALADIN.add_spell(spell_id=31884, cooldown=120, duration=20) # Wings
PALADIN_HOLY.add_spell(spell_id=31821, cooldown=180, duration=8) # Aura Mastery


HUNTER.add_spell(spell_id=328231, cooldown=120, duration=15) # Covenant: Wild Spirits
HUNTER_BEASTMASTERY.add_spell(spell_id=193530, cooldown=180, duration=20) # Aspect of the Wild
HUNTER_BEASTMASTERY.add_spell(spell_id=19574, cooldown=90, duration=15, show=False) # Bestial Wrath
HUNTER_BEASTMASTERY.add_spell(spell_id=201430, cooldown=120, duration=12, show=False) # Stampede
# HUNTER_SURVIVAL.add_spell(spell_id=266779, cooldown=120, duration=20) # Coordinated Assault
HUNTER_MARKSMANSHIP.add_spell(spell_id=288613, cooldown=120, duration=15, show=False) # Trueshot

# Rogue

# Priest
# PRIEST_SHADOW.add_spell(spell_id=34433, cooldown=180, duration=15) # Shadowfiend
# PRIEST_SHADOW.add_spell(spell_id=228260, cooldown=90) # Void Erruption
# PRIEST_DISCIPLINE.add_spell(spell_id=34433, cooldown=180, duration=15, show=False) # Shadowfiend
#TODO: add mindbender?
PRIEST_DISCIPLINE.add_spell(spell_id=62618,  cooldown=180, duration=10)  #Power Word: Cuddle
PRIEST_DISCIPLINE.add_spell(spell_id=109964,  cooldown=60, duration=10)  # Spirit Shell
PRIEST_DISCIPLINE.add_spell(spell_id=47536,  cooldown=90, duration=8, show=False)  # Rapture
PRIEST_DISCIPLINE.add_spell(spell_id=246287,  cooldown=90, show=False)  # Evengelism
PRIEST_HOLY.add_spell(spell_id=64843, cooldown=180, duration=8) # Hymn
PRIEST_HOLY.add_spell(spell_id=265202, cooldown=240) # Savl (not showing CD, because dynamic)
PRIEST_HOLY.add_spell(spell_id=200183, cooldown=120, duration=20, show=False) # Apotheosis

# DK
DEATHKNIGHT.add_spell(spell_id=51052, cooldown=120, duration=10, show=False)  # Anti-Magic Zone
DEATHKNIGHT_UNHOLY.add_spell(spell_id=42650, cooldown=4*60, duration=30)  # Army (usually 4min with talent)
DEATHKNIGHT_UNHOLY.add_spell(spell_id=275699, cooldown=60, duration=15, show=False)  # Apocalypse (90sec -> 60sec talent)


# Shamans
SHAMAN_RESTORATION.add_spell(spell_id=108280, cooldown=180, duration=10) # Healing Tide
SHAMAN_RESTORATION.add_spell(spell_id=98008,  cooldown=180, duration=6)  # Spirit Link
SHAMAN_RESTORATION.add_spell(spell_id=16191,  cooldown=180, duration=8, show=False)  # Mana Tide
SHAMAN_RESTORATION.add_spell(spell_id=207399,  cooldown=300, duration=30)  # Ahnk totem
SHAMAN_RESTORATION.add_spell(spell_id=114052,  cooldown=180, duration=15)  # Ascendance

# Mage
MAGE.add_spell(spell_id=314791, cooldown=60, duration=3.1, show=False) # Shifting Power
MAGE_FIRE.add_spell(spell_id=190319, cooldown=60, duration=10) # Combustion
MAGE_FIRE.add_spell(spell_id=153561, cooldown=45, show=False) # Meteor

# Warlock
WARLOCK.add_spell(spell_id=325640, cooldown=60, duration=8, show=False) # Soulrot

WARLOCK_AFFLICTION.add_spell(spell_id=205180, cooldown=180, duration=8) # Darkglare
WARLOCK_AFFLICTION.add_spell(spell_id=113860, cooldown=120, duration=20) # Dark Soul: Misery
WARLOCK_AFFLICTION.add_spell(spell_id=205179, cooldown=45, duration=16) # PS

WARLOCK_DEMONOLOGY.add_spell(spell_id=265187, cooldown=90, duration=15) # Tyrant
WARLOCK_DEMONOLOGY.add_spell(spell_id=111898, cooldown=120, duration=17) # Felguard
WARLOCK_DEMONOLOGY.add_spell(spell_id=267217, cooldown=180, duration=15) # Netherportal

WARLOCK_DESTRUCTION.add_spell(spell_id=1122, cooldown=180, duration=30) # Infernal
WARLOCK_DESTRUCTION.add_spell(spell_id=113858, cooldown=120, duration=20) # Dark Soul: Instability

# Monk
MONK.add_spell(spell_id=115203,  cooldown=360, duration=15, show=False) # Fort Brew
MONK.add_spell(spell_id=310454,  cooldown=120, duration=30, show=False) # Weapons of Order
MONK_MISTWEAVER.add_spell(spell_id=322118,  cooldown=180, duration=3.5) # Yulon
MONK_MISTWEAVER.add_spell(spell_id=115310,  cooldown=180) # Revival
MONK_MISTWEAVER.add_spell(spell_id=325197,  cooldown=180) # Chiji

# Druid
DRUID.add_spell(spell_id=323764, cooldown=120, duration=4)  # Convoke
DRUID_RESTORATION.add_spell(spell_id=197721, cooldown=90, duration=8, show=False) # Flourish
DRUID_RESTORATION.add_spell(spell_id=29166, cooldown=180, duration=10, show=False) # Innervate
DRUID_RESTORATION.add_spell(spell_id=740, cooldown=180, duration=6) # Tranquility
DRUID_RESTORATION.add_spell(spell_id=33891, cooldown=180, duration=30) # Tree of Life

DRUID_BALANCE.add_spell(spell_id=194223, cooldown=180, duration=20) # Celestrial
DRUID_BALANCE.add_spell(spell_id=102560, cooldown=180, duration=30) # Incarnation
DRUID_BALANCE.add_spell(spell_id=205636, cooldown=60, duration=10, show=False) # Treants
DRUID_BALANCE.add_spell(spell_id=202770, cooldown=60, duration=8, show=False) # Fury of Elune

# DH
DEMONHUNTER.add_spell(spell_id=306830, cooldown=60) # Elysian Decree
DEMONHUNTER.add_spell(spell_id=323639, cooldown=90) # The Hunt
DEMONHUNTER.add_spell(spell_id=317009, cooldown=60) # Sinful Brand

DEMONHUNTER_HAVOC.add_spell(spell_id=200166, cooldown=300, duration=30) # Meta
DEMONHUNTER_HAVOC.add_spell(spell_id=196718, cooldown=180, duration=8, show=False) # Darkness
DEMONHUNTER_HAVOC.add_spell(spell_id=196555, cooldown=180, duration=5, show=False) # Netherwalk

################################################################################
# Potions (figure out how to best include them later)

# 307162 # Int
# 307159 # Agi
# 307164 # Str

for spec in HEALS:
    spec.add_spell(spell_id=307161, cooldown=300, duration=10, show=False) # Mana Channel Pot

for spec in MELEE+RANGE:
    spec.add_spell(spell_id=307495, cooldown=300, duration=25, show=False) # Phantom Fire

for spec in [PRIEST_SHADOW, SHAMAN_ELEMENTAL, MAGE, WARLOCK, DRUID_BALANCE]:
    spec.add_spell(spell_id=307162, cooldown=300, duration=25, show=False) # Intellect Pot

for spec in [HUNTER, ROGUE, SHAMAN_ENHANCEMENT, MONK_WINDWALKER, DRUID_FERAL, DEMONHUNTER]:
    spec.add_spell(spell_id=307159, cooldown=300, duration=25, show=False) # Agility Pot

for spec in [WARRIOR, PALADIN_RETRIBUTION, DEATHKNIGHT]:
    spec.add_spell(spell_id=307159, cooldown=300, duration=25, show=False) # Agility Pot


################################################################################
# Trinkets

# 330323 # IQC
# 345539 # Ordnance
SPELLS = {spell_id: spell for spell_id, spell in m.WoWSpell._all.items() if spell_id > 0}

