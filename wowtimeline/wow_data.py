
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
WARRIOR_PROTECTION.short_name = "Prot"

PALADIN = m.WoWClass(name="Paladin")
PALADIN_HOLY = PALADIN.add_spec(name="Holy", role=HEAL)
PALADIN_PROTECTION = PALADIN.add_spec(name="Protection", role=TANK)
PALADIN_PROTECTION.short_name = "Prot"
PALADIN_RETRIBUTION = PALADIN.add_spec(name="Retribution", role=MDPS)
PALADIN_RETRIBUTION.short_name = "Ret"

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
PRIEST_DISCIPLINE.short_name = "Disc"
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
SHAMAN_RESTORATION.short_name = "Resto"

MAGE = m.WoWClass(name="Mage")
MAGE_ARCANE = MAGE.add_spec(name="Arcane", role=RDPS)
MAGE_FIRE = MAGE.add_spec(name="Fire", role=RDPS)
MAGE_FROST = MAGE.add_spec(name="Frost", role=RDPS)

WARLOCK = m.WoWClass(name="Warlock")
WARLOCK_AFFLICTION = WARLOCK.add_spec(name="Affliction", role=RDPS)
WARLOCK_AFFLICTION.short_name = "Aff"
WARLOCK_DEMONOLOGY = WARLOCK.add_spec(name="Demonology", role=RDPS)
WARLOCK_DEMONOLOGY.short_name = "Demo"
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
DRUID_RESTORATION.short_name = "Resto"

DEMONHUNTER = m.WoWClass(name="Demon Hunter")
DEMONHUNTER_HAVOC = DEMONHUNTER.add_spec(name="Havoc", role=MDPS)
DEMONHUNTER_VENGEANCE = DEMONHUNTER.add_spec(name="Vengeance", role=TANK)


OTHER = m.WoWClass(name="Other")
OTHER_POTION = OTHER.add_spec(name="Potion", role="other")
OTHER_TRINKET = OTHER.add_spec(name="Trinkets", role="other")



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
# SHAMAN_ELEMENTAL.supported = False
# SHAMAN_ENHANCEMENT.supported = False
# SHAMAN_RESTORATION.supported = False
MAGE_ARCANE.supported = False
# MAGE_FIRE.supported = False
MAGE_FROST.supported = False
# WARLOCK_AFFLICTION.supported = False
# WARLOCK_DEMONOLOGY.supported = False
# WARLOCK_DESTRUCTION.supported = False
MONK_BREWMASTER.supported = False
# MONK_MISTWEAVER.supported = False
# MONK_WINDWALKER.supported = False
# DRUID_BALANCE.supported = False
DRUID_FERAL.supported = False
DRUID_GUARDIAN.supported = False
# DRUID_RESTORATION.supported = False
# DEMONHUNTER_HAVOC.supported = False
DEMONHUNTER_VENGEANCE.supported = False


# Warcraft Logs: Class IDs
DEATHKNIGHT.id = 1
DRUID.id = 2
HUNTER.id = 3
MAGE.id = 4
MONK.id = 5
PALADIN.id = 6
PRIEST.id = 7
ROGUE.id = 8
SHAMAN.id = 9
WARLOCK.id = 10
WARRIOR.id = 11
DEMONHUNTER.id = 12

# Warcraft Logs: Spec IDs
DEATHKNIGHT_BLOOD.id = 1
DEATHKNIGHT_FROST.id = 2
DEATHKNIGHT_UNHOLY.id = 3
DRUID_BALANCE.id  = 1
DRUID_FERAL.id = 2
DRUID_GUARDIAN.id = 3
DRUID_RESTORATION.id = 4
HUNTER_BEASTMASTERY.id = 1
HUNTER_MARKSMANSHIP.id = 2
HUNTER_SURVIVAL.id = 3
MAGE_ARCANE.id = 1
MAGE_FIRE.id = 2
MAGE_FROST.id = 3
MONK_BREWMASTER.id = 1
MONK_MISTWEAVER.id = 2
MONK_WINDWALKER.id = 3
PALADIN_HOLY.id = 1
PALADIN_PROTECTION.id = 2
PALADIN_RETRIBUTION.id = 3
PRIEST_DISCIPLINE.id = 1
PRIEST_HOLY.id = 2
PRIEST_SHADOW.id = 3
ROGUE_ASSASSINATION.id = 1
ROGUE_OUTLAW.id = 4
ROGUE_SUBTLETY.id = 3
SHAMAN_ELEMENTAL.id = 1
SHAMAN_ENHANCEMENT.id = 2
SHAMAN_RESTORATION.id = 3
WARLOCK_AFFLICTION.id = 1
WARLOCK_DEMONOLOGY.id = 2
WARLOCK_DESTRUCTION.id = 3
WARRIOR_ARMS.id = 1
WARRIOR_FURY.id = 2
WARRIOR_PROTECTION.id = 3
DEMONHUNTER_HAVOC.id = 1
DEMONHUNTER_VENGEANCE.id = 2

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


ROLES = [
    {"slug": TANK, "name": "Tank"},
    {"slug": HEAL, "name": "Healer"},
    {"slug": RDPS, "name": "Range"},
    {"slug": MDPS, "name": "Melee"},
]
for role in ROLES:
    role["specs"] = [spec for spec in SPECS if spec.role == role["slug"]]


class_by_name = {c.name: c for c in CLASSES}
spec_by_full_name = {s.full_name: s for s in SPECS}


# OTHER
POTIONS_GRP = "90_Potion"
spec_by_full_name[POTIONS_GRP] = OTHER_POTION
TRINKET_GRP = "80_Trinket"
spec_by_full_name[TRINKET_GRP] = OTHER_TRINKET


# common heal Comps to check
HEAL_COMPS = [
    {
        "specs": [PALADIN_HOLY, PRIEST_DISCIPLINE, SHAMAN_RESTORATION, DRUID_RESTORATION],
        "extra_filter": "source.role='healer'",
    },

    {
        "specs": [PALADIN_HOLY, PRIEST_DISCIPLINE, SHAMAN_RESTORATION, SHAMAN_RESTORATION],
        "extra_filter": "source.role='healer'",
    },

    {
        "specs": [PALADIN_HOLY, PRIEST_HOLY, PRIEST_DISCIPLINE, SHAMAN_RESTORATION, SHAMAN_RESTORATION],
        "extra_filter": "source.role='healer'",
    }
]

for comp in HEAL_COMPS:
    specs = comp.get("specs", [])
    comp["search"] = ",".join(f"{s.class_.id}.{s.id}.{specs.count(s)}" for s in SPECS if s in specs)
    comp["name"] = "_".join(spec.full_name_slug for spec in specs)

# todo: filter for ventyr/kryan pala
# "abilities.316958", # Ventyr Pala (WARNING! Could be a ret)


################################################################################
# Define all the spells we care about
#
CD1min = 1 * 60 # 60
CD2min = 2 * 60 # 120
CD3min = 3 * 60 # 180
CD4min = 4 * 60 # 240
CD5min = 5 * 60 # 300

# DPS CDs
# WARRIOR.add_spell(spell_id=97462, cooldown=180, duration=10) # Rally Cry
# WARRIOR.add_spell(spell_id=107574, cooldown=90, duration=20) # Avatar
# WARRIOR.add_spell(spell_id=1719, cooldown=90, duration=10) # Recklessness

# PALADIN.add_spell(spell_id=105809, cooldown=180, duration=20, show=False) # Holy Avenger
PALADIN.add_spell(spell_id=304971, cooldown=CD1min, show=False) # Covenant: Divine Toll
PALADIN.add_spell(spell_id=316958, cooldown=CD4min, duration=30) # Covenant: Ashen Hallow
PALADIN.add_spell(spell_id=31884, cooldown=CD2min, duration=20) # Wings
PALADIN_HOLY.add_spell(spell_id=31821, cooldown=CD3min, duration=8) # Aura Mastery

HUNTER.add_spell(spell_id=328231, cooldown=120, duration=15) # Covenant: Wild Spirits
HUNTER_BEASTMASTERY.add_spell(spell_id=193530, cooldown=180, duration=20) # Aspect of the Wild
HUNTER_BEASTMASTERY.add_spell(spell_id=19574, cooldown=90, duration=15, show=False) # Bestial Wrath
HUNTER_BEASTMASTERY.add_spell(spell_id=201430, cooldown=120, duration=12, show=False) # Stampede
# HUNTER_SURVIVAL.add_spell(spell_id=266779, cooldown=120, duration=20) # Coordinated Assault
HUNTER_MARKSMANSHIP.add_spell(spell_id=288613, cooldown=120, duration=15, show=False) # Trueshot

# Rogue

# Priest
PRIEST.add_spell(spell_id=10060, cooldown=CD2min, duration=20) # Power Infusion
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
SHAMAN.add_spell(spell_id=326059, cooldown=45, show=False)  # Necro: Primordial Wave
SHAMAN.add_spell(spell_id=320674, cooldown=90, show=False)  # Ventyr: Chain Harvest
SHAMAN_ELEMENTAL.add_spell(spell_id=191634, cooldown=60, show=True)  # Stormkeeper
SHAMAN_ELEMENTAL.add_spell(spell_id=198067, cooldown=150, show=True)  # Fire Elemental

SHAMAN_ENHANCEMENT.add_spell(spell_id=114051, cooldown=CD3min, show=True)  # Ascendance
SHAMAN_ENHANCEMENT.add_spell(spell_id=51533, cooldown=CD2min, show=True)  # Feral Spirit

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
MONK.add_spell(spell_id=322109, cooldown=180) # Touch of Death
MONK.add_spell(spell_id=115203, cooldown=360, duration=15, show=False) # Fort Brew
MONK.add_spell(spell_id=310454, cooldown=120, duration=30, show=False) # Weapons of Order

MONK_MISTWEAVER.add_spell(spell_id=322118, cooldown=180, duration=3.5) # Yulon
MONK_MISTWEAVER.add_spell(spell_id=115310, cooldown=180) # Revival
MONK_MISTWEAVER.add_spell(spell_id=325197, cooldown=180) # Chiji

MONK_WINDWALKER.add_spell(spell_id=123904, cooldown=120, duration=24) # Xuen
MONK_WINDWALKER.add_spell(spell_id=137639, cooldown=90, duration=15) # Storm, Earth and Fire


# Druid
DRUID.add_spell(spell_id=323764, cooldown=120, duration=4, show=False)  # Convoke
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

DEMONHUNTER_HAVOC.add_spell(spell_id=200166, cooldown=CD4min, duration=30) # Meta
DEMONHUNTER_HAVOC.add_spell(spell_id=196718, cooldown=180, duration=8, show=False) # Darkness
DEMONHUNTER_HAVOC.add_spell(spell_id=196555, cooldown=180, duration=5, show=False) # Netherwalk

################################################################################
# Potions (figure out how to best include them later)


for spec in HEALS:
    spec.add_spell(group=OTHER_POTION, spell_id=307161, cooldown=300, duration=10, show=False) # Mana Channel Pot
    spec.add_spell(group=OTHER_POTION, spell_id=307193, cooldown=300, show=False)              # Mana Pot
    spec.add_spell(group=OTHER_POTION, spell_id=307162, cooldown=300, duration=25, show=False) # Intellect Pot
    spec.add_spell(group=OTHER_POTION, spell_id=307495, cooldown=300, duration=25, show=False) # Phantom Fire

for spec in MELEE+RANGE:
    spec.add_spell(group=OTHER_POTION, spell_id=307495, cooldown=300, duration=25, show=False) # Phantom Fire

for spec in [PRIEST_SHADOW, SHAMAN_ELEMENTAL, MAGE, WARLOCK, DRUID_BALANCE]:
    spec.add_spell(group=OTHER_POTION, spell_id=307162, cooldown=300, duration=25, show=False) # Intellect Pot

for spec in [HUNTER, ROGUE, SHAMAN_ENHANCEMENT, MONK_WINDWALKER, DRUID_FERAL, DEMONHUNTER]:
    spec.add_spell(group=OTHER_POTION, spell_id=307159, cooldown=300, duration=25, show=False) # Agility Pot

for spec in [WARRIOR, PALADIN_RETRIBUTION, DEATHKNIGHT]:
    spec.add_spell(group=OTHER_POTION, spell_id=307164, cooldown=300, duration=25, show=False) # Strength Pot


################################################################################
# All Classes
for spec in SPECS:

    spec.add_spell(group=OTHER_POTION, spell_id=6262, show=False) # Healthstone
    spec.add_spell(group=OTHER_POTION, spell_id=307192, cooldown=CD5min, show=False) # Healthpot

    # Raid Trinkets
    spec.add_spell(group=OTHER_TRINKET, spell_id=349857, cooldown=90, show=False) # Dreadfire Vessel
    spec.add_spell(group=OTHER_TRINKET, spell_id=345019, cooldown=90, show=False) # Skulking Predator
    spec.add_spell(group=OTHER_TRINKET, spell_id=345251, cooldown=60, duration=15, show=False) # Soul Igniter

    # Dungeon Trinkets
    spec.add_spell(group=OTHER_TRINKET, spell_id=330323, cooldown=CD3min, show=False) # Quantum Device
    spec.add_spell(group=OTHER_TRINKET, spell_id=345539, cooldown=CD3min, duration=35, show=False) # Ordnance (estimated duration)
    spec.add_spell(group=OTHER_TRINKET, spell_id=345530, cooldown=90, duration=6, show=False) # Overcharged Anima Battery
    spec.add_spell(group=OTHER_TRINKET, spell_id=345801, cooldown=CD2min, duration=15, show=False) # Soulletting Ruby

    # Other Trinkets
    spec.add_spell(group=OTHER_TRINKET, spell_id=348139, cooldown=90, duration=9, show=False) # Divine Bell
    spec.add_spell(group=OTHER_TRINKET, spell_id=345228, cooldown=CD1min, duration=15, show=False) # Badge

# 345539 # Ordnance



SPELLS = {spell_id: spell for spell_id, spell in m.WoWSpell._all.items() if spell_id > 0}



