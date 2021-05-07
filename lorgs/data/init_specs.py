#!/usr/bin/env python
"""Models for Raids and RaidBosses."""

# pylint: disable=line-too-long
# pylint: disable=C0326  # spaces

# IMPORT THIRD PARTY LIBRARIES
import dotenv
dotenv.load_dotenv() # pylint: disable=wrong-import-position

# IMPORT LOCAL LIBRARIES
from lorgs import db
from lorgs.models.specs import WowClass
from lorgs.models.specs import WowRole
from lorgs.models.specs import WowSpec


################################################################################
#
#   ROLES
#
################################################################################
TANK = WowRole(id=10, code="tank", name="Tank")
HEAL = WowRole(id=20, code="heal", name="Healer")
MDPS = WowRole(id=30, code="mdps", name="Melee")
RDPS = WowRole(id=40, code="rdps", name="Range")


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

ROLE_ITEM = WowRole(id=1001, code="item", name="Items")
OTHER = WowClass(id=1001, name="Other", color="#cccccc")
OTHER_POTION  = WowSpec(id=1001, role=ROLE_ITEM, wow_class=OTHER,  name="Potions")
OTHER_TRINKET = WowSpec(id=1002, role=ROLE_ITEM, wow_class=OTHER,  name="Trinkets")


################################################################################
#
#   add them to the DB
#

# going by roles, to save typing
ROLES = [TANK, HEAL, MDPS, RDPS, ROLE_ITEM]
db.session.add_all(ROLES)
db.session.commit()
db.session.remove()
