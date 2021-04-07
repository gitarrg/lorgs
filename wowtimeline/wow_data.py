


from wowtimeline import models as m


# ROLES
TANK = "tank"
HEAL = "heal"
MDPS = "dps"
RDPS = "dps"


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
#
# ids are based of:
# https://www.warcraftlogs.com/v1/classes
#

# DEATHKNIGHT = m.WoWClass(class_id=1, name="Death Knight")
# DEATHKNIGHT_BLOOD = DEATHKNIGHT.add_spec(spec_id=1, name="Blood")
# DEATHKNIGHT_FROST = DEATHKNIGHT.add_spec(spec_id=2, name="Frost")
# DEATHKNIGHT_UNHOLY = DEATHKNIGHT.add_spec(spec_id=3, name="Unholy")

DRUID = m.WoWClass(class_id=2, name="Druid")
# DRUID_BALANCE = DRUID.add_spec(spec_id=1, name="Balance")
# DRUID_FERAL = DRUID.add_spec(spec_id=2, name="Feral")
# DRUID_GUARDIAN = DRUID.add_spec(spec_id=3, name="Guardian")
DRUID_RESTORATION = DRUID.add_spec(spec_id=4, name="Restoration", role=HEAL)

HUNTER = m.WoWClass(class_id=3, name="Hunter")
HUNTER_BEASTMASTERY = HUNTER.add_spec(spec_id=1, name="Beast Mastery")
HUNTER_MARKSMANSHIP = HUNTER.add_spec(spec_id=2, name="Marksmanship")
# HUNTER_SURVIVAL = HUNTER.add_spec(spec_id=3, name="Survival")

MAGE = m.WoWClass(class_id=4, name="Mage")
# MAGE_ARCANE = MAGE.add_spec(spec_id=1, name="Arcane")
MAGE_FIRE = MAGE.add_spec(spec_id=2, name="Fire")
# MAGE_FROST = MAGE.add_spec(spec_id=3, name="Frost")

# MONK = m.WoWClass(class_id=5, name="Monk")
# MONK_BREWMASTER = MONK.add_spec(spec_id=1, name="Brewmaster")
# MONK_MISTWEAVER = MONK.add_spec(spec_id=2, name="Mistweaver", role=HEAL)
# MONK_WINDWALKER = MONK.add_spec(spec_id=3, name="Windwalker")

PALADIN = m.WoWClass(class_id=6, name="Paladin")
PALADIN_HOLY = PALADIN.add_spec(spec_id=1, name="Holy", role=HEAL)
# PALADIN_PROTECTION = PALADIN.add_spec(spec_id=2, name="Protection")
# PALADIN_RETRIBUTION = PALADIN.add_spec(spec_id=3, name="Retribution")

PRIEST = m.WoWClass(class_id=7, name="Priest")
PRIEST_DISCIPLINE = PRIEST.add_spec(spec_id=1, name="Discipline", role=HEAL)
PRIEST_HOLY = PRIEST.add_spec(spec_id=2, name="Holy", role=HEAL)
# PRIEST_SHADOW = PRIEST.add_spec(spec_id=3, name="Shadow")

# ROGUE = m.WoWClass(class_id=8, name="Rogue")
# ROGUE_ASSASSINATION = ROGUE.add_spec(spec_id=1, name="Assassination")
# ROGUE_SUBTLETY = ROGUE.add_spec(spec_id=3, name="Subtlety")
# ROGUE_OUTLAW = ROGUE.add_spec(spec_id=4, name="Outlaw")

SHAMAN = m.WoWClass(class_id=9, name="Shaman")
# SHAMAN_ELEMENTAL = SHAMAN.add_spec(spec_id=1, name="Elemental")
# SHAMAN_ENHANCEMENT = SHAMAN.add_spec(spec_id=2, name="Enhancement")
SHAMAN_RESTORATION = SHAMAN.add_spec(spec_id=3, name="Restoration", role=HEAL)

WARLOCK = m.WoWClass(class_id=10, name="Warlock")
WARLOCK_AFFLICTION = WARLOCK.add_spec(spec_id=1, name="Affliction")
# WARLOCK_DEMONOLOGY = WARLOCK.add_spec(spec_id=2, name="Demonology")
WARLOCK_DESTRUCTION = WARLOCK.add_spec(spec_id=3, name="Destruction")

# WARRIOR = m.WoWClass(class_id=11, name="Warrior")
# WARRIOR_ARMS = WARRIOR.add_spec(spec_id=1, name="Arms")
# WARRIOR_FURY = WARRIOR.add_spec(spec_id=2, name="Fury")
# WARRIOR_PROTECTION = WARRIOR.add_spec(spec_id=3, name="Protection")

# DEMONHUNTER = m.WoWClass(class_id=12, name="Demon Hunter")
# DEMONHUNTER_HAVOC = DEMONHUNTER.add_spec(spec_id=1, name="Havoc")
# DEMONHUNTER_VENGEANCE = DEMONHUNTER.add_spec(spec_id=2, name="Vengeance")


################################################################################
# Define all the spells we care about
#

# DPS CDs
# WARRIOR.add_spell(spell_id=97462, cooldown=180, duration=10) # Rally Cry
# WARRIOR.add_spell(spell_id=107574, cooldown=90, duration=20) # Avatar
# WARRIOR.add_spell(spell_id=1719, cooldown=90, duration=10) # Recklessness

PALADIN.add_spell(spell_id=105809, cooldown=180, duration=20) # Holy Avenger
PALADIN.add_spell(spell_id=304971, cooldown=60) # Covenant: Divine Toll
PALADIN.add_spell(spell_id=316958, cooldown=240, duration=30) # Covenant: Ashen Hallow
PALADIN.add_spell(spell_id=31884, cooldown=120, duration=20) # Wings
PALADIN_HOLY.add_spell(spell_id=31821, cooldown=180, duration=8) # Aura Mastery
# PALADIN_RETRIBUTION.add_spell(spell_id=231895, cooldown=120, duration=25) # Crusade

HUNTER.add_spell(spell_id=328231, cooldown=120, duration=15) # Covenant: Wild Spirits
HUNTER_BEASTMASTERY.add_spell(spell_id=193530, cooldown=180, duration=20) # Aspect of the Wild
HUNTER_BEASTMASTERY.add_spell(spell_id=19574, cooldown=90, duration=15) # Bestial Wrath
HUNTER_BEASTMASTERY.add_spell(spell_id=201430, cooldown=120, duration=12) # Stampede
# HUNTER_SURVIVAL.add_spell(spell_id=266779, cooldown=120, duration=20) # Coordinated Assault
HUNTER_MARKSMANSHIP.add_spell(spell_id=288613, cooldown=120, duration=15) # Trueshot

# Rogue

# PRIEST_SHADOW.add_spell(spell_id=34433, cooldown=180, duration=15) # Shadowfiend
# PRIEST_SHADOW.add_spell(spell_id=228260, cooldown=90) # Void Erruption
PRIEST_DISCIPLINE.add_spell(spell_id=34433, cooldown=180, duration=15) # Shadowfiend
PRIEST_DISCIPLINE.add_spell(spell_id=62618,  cooldown=180, duration=10)  #Power Word: Cuddle
PRIEST_DISCIPLINE.add_spell(spell_id=109964,  cooldown=60, duration=10)  # Spirit Shell
PRIEST_DISCIPLINE.add_spell(spell_id=47536,  cooldown=90, duration=8)  # Rapture
PRIEST_DISCIPLINE.add_spell(spell_id=246287,  cooldown=90)  # Evengelism
PRIEST_HOLY.add_spell(spell_id=64843, cooldown=180, duration=8) # Hymn
PRIEST_HOLY.add_spell(spell_id=265202) # Savl (not showing CD, because dynamic)
PRIEST_HOLY.add_spell(spell_id=200183, cooldown=120, duration=20) # Apotheosis


# DK
# DEATHKNIGHT.add_spell(spell_id=51052, cooldown=120, duration=10)  # Anti-Magic Zone)

# Shamans
SHAMAN_RESTORATION.add_spell(spell_id=108280, cooldown=180, duration=10) # Healing Tide
SHAMAN_RESTORATION.add_spell(spell_id=98008,  cooldown=180, duration=6)  # Spirit Link
SHAMAN_RESTORATION.add_spell(spell_id=16191,  cooldown=180, duration=8)  # Mana Tide
SHAMAN_RESTORATION.add_spell(spell_id=207399,  cooldown=300, duration=30)  # Ahnk totem
SHAMAN_RESTORATION.add_spell(spell_id=114052,  cooldown=180, duration=15)  # Ascendance

MAGE.add_spell(spell_id=314791, cooldown=60, duration=3.1) # Shifting Power
MAGE_FIRE.add_spell(spell_id=190319, cooldown=120, duration=10) # Combustion

WARLOCK.add_spell(spell_id=325640, cooldown=60, duration=8) # Soulrot
# WARLOCK_AFFLICTION.add_spell(spell_id=325640, cooldown=60, duration=8) # Soulrot
WARLOCK_AFFLICTION.add_spell(spell_id=205180, cooldown=180, duration=8) # Darkglare
WARLOCK_AFFLICTION.add_spell(spell_id=113860, cooldown=120, duration=20) # Dark Soul: Misery
# WARLOCK_DEMONOLOGY.add_spell(spell_id=265187, cooldown=180, duration=15) # Tyrant
WARLOCK_DESTRUCTION.add_spell(spell_id=1122, cooldown=180, duration=30) # Infernal
WARLOCK_DESTRUCTION.add_spell(spell_id=113858, cooldown=120, duration=20) # Dark Soul: Instability

# Monk
# MONK_MISTWEAVER.add_spell(spell_id=115310,  cooldown=300) # Revival

# Druid
DRUID.add_spell(spell_id=323764, cooldown=120)  # Convoke
DRUID_RESTORATION.add_spell(spell_id=197721, cooldown=90, duration=8) # Flourish
DRUID_RESTORATION.add_spell(spell_id=29166, cooldown=180, duration=10) # Innervate
DRUID_RESTORATION.add_spell(spell_id=740, cooldown=180, duration=6) # Tranquility
DRUID_RESTORATION.add_spell(spell_id=33891, cooldown=180, duration=30) # Tree of Life


# DH
# DEMONHUNTER_HAVOC.add_spell(spell_id=196718, cooldown=180, duration=8) # Darkness


################################################################################
# Alias to some full lists
# (these are dicts.. so they will be filled later)
#
CLASSES = m.WoWClass._all
SPELLS = {spell_id: spell for spell_id, spell in m.WoWSpell._all.items() if spell_id > 0}


# SPECS = {}
# for i, wow_class in CLASSES.items():
#     for j, spec in specs.items():
#         SPECS[(i,j)] = spec

