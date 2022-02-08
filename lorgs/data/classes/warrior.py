"""Define the Priest Class its Specs and Spells."""
# pylint: disable=line-too-long
# pylint: disable=bad-whitespace
# pylint: disable=wildcard-import
# pylint: disable=unused-wildcard-import

# IMPORT LOCAL LIBRARIES
from lorgs.data.constants import *
from lorgs.data.roles import *
from lorgs.models.wow_class import WowClass
from lorgs.models.wow_spec import WowSpec


################################################################################
# Class
#
WARRIOR = WowClass(id=1, name="Warrior", color="#C69B6D")

################################################################################
# Specs
#
WARRIOR_ARMS          = WowSpec(role=MDPS, wow_class=WARRIOR,      name="Arms")
WARRIOR_FURY          = WowSpec(role=MDPS, wow_class=WARRIOR,      name="Fury")
WARRIOR_PROTECTION    = WowSpec(role=TANK, wow_class=WARRIOR,      name="Protection",    short_name="Prot")

################################################################################
# Spells
#
WARRIOR.add_spell(             spell_id=324143, cooldown=120, duration=15, color=COL_NECRO, name="Conqueror's Banner",  icon="ability_maldraxxus_warriorplantbanner.jpg")
WARRIOR.add_spell(             spell_id=325886, cooldown=75,  duration=12, color=COL_NF,    name="Ancient Aftershock",  icon="ability_ardenweald_warrior.jpg")  # 15sec CD reduction with Conduit
WARRIOR.add_spell(             spell_id=307865, cooldown=60,               color=COL_KYR,   name="Spear of Bastion",    icon="ability_bastion_warrior.jpg")
WARRIOR.add_spell(             spell_id=97462,  cooldown=180, duration=10,                  name="Rallying Cry",        icon="ability_warrior_rallyingcry.jpg",           show=False, spell_type=SPELL_TYPE_RAID)
WARRIOR.add_spell(             spell_id=23920,  cooldown=10,  duration=5,                   name="Spell Reflection",    icon="ability_warrior_shieldreflection.jpg",      show=False)

WARRIOR_ARMS.add_spell(        spell_id=107574, cooldown=90,  duration=20,                  name="Avatar",              icon="warrior_talent_icon_avatar.jpg")
WARRIOR_ARMS.add_spell(        spell_id=227847, cooldown=90,  duration=6,                   name="Bladestorm",          icon="ability_warrior_bladestorm.jpg")
WARRIOR_ARMS.add_spell(        spell_id=262161, cooldown=45,  duration=10,                  name="Warbreaker",          icon="inv_warbreaker.jpg",                        show=False)
WARRIOR_ARMS.add_spell(        spell_id=772,    cooldown=15,                                name="Rend",                icon="ability_gouge.jpg",                         show=False)
WARRIOR_ARMS.add_spell(        spell_id=118038, cooldown=120, duration=8,                   name="Die by the Sword",    icon="ability_warrior_challange.jpg",             show=False)

WARRIOR_FURY.add_spell(        spell_id=1719,   cooldown=60,  duration=10,                  name="Recklessness",        icon="warrior_talent_icon_innerrage.jpg")
WARRIOR_FURY.add_spell(        spell_id=46924,  cooldown=60,  duration=4,                   name="Bladestorm",          icon="ability_warrior_bladestorm.jpg")

WARRIOR_PROTECTION.add_spell(  spell_id=107574, cooldown=50,  duration=20,                  name="Avatar",              icon="warrior_talent_icon_avatar.jpg",            show=False)  # CD reduced by Talent per Rage spend
WARRIOR_PROTECTION.add_spell(  spell_id=12975,  cooldown=180, duration=15, color="#ffbf29", name="Last Stand",          icon="spell_holy_ashestoashes.jpg")
WARRIOR_PROTECTION.add_spell(  spell_id=871,    cooldown=120, duration=8,  color="#039dfc", name="Shield Wall",         icon="ability_warrior_shieldwall.jpg")  # CD reduced by Talent per Rage spend
