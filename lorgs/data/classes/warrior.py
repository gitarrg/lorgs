"""Define the Priest Class its Specs and Spells."""
# pylint: disable=line-too-long
# pylint: disable=bad-whitespace
# pylint: disable=wildcard-import
# pylint: disable=unused-wildcard-import
# fmt: off

# IMPORT LOCAL LIBRARIES
from lorgs.data.constants import *
from lorgs.data.roles import *
from lorgs.models.wow_class import WowClass
from lorgs.models.wow_spec import WowSpec
from lorgs.models.wow_spell import SpellTag, SpellType


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
WARRIOR.add_spell(             spell_id=376079, cooldown=90,  duration=4,  color=COL_KYR,   name="Spear of Bastion",    icon="ability_bastion_warrior.jpg")
WARRIOR.add_spell(             spell_id=384318, cooldown=90,  duration=8,  color="#d13b59", name="Thunderous Roar",     icon="ability_warrior_dragonroar.jpg",            show=False)
WARRIOR.add_spell(             spell_id=97462,  cooldown=180, duration=10,                  name="Rallying Cry",        icon="ability_warrior_rallyingcry.jpg",           show=False, spell_type=SpellType.RAID, tags=[SpellTag.RAID_CD])
WARRIOR.add_spell(             spell_id=23920,  cooldown=10,  duration=5,                   name="Spell Reflection",    icon="ability_warrior_shieldreflection.jpg",      show=False)
WARRIOR.add_spell(             spell_id=107574, cooldown=90,  duration=20,                  name="Avatar",              icon="warrior_talent_icon_avatar.jpg",            show=False)
WARRIOR.add_spell(             spell_id=228920, cooldown=90,  duration=12, color="#d1793b", name="Ravager",             icon="warrior_talent_icon_ravager.jpg")

WARRIOR_ARMS.add_spell(        spell_id=389774, cooldown=90,  duration=6,                   name="Bladestorm",          icon="ability_warrior_bladestorm.jpg")
WARRIOR_ARMS.add_spell(        spell_id=262161, cooldown=45,  duration=10,                  name="Warbreaker",          icon="inv_warbreaker.jpg",                        show=False)
WARRIOR_ARMS.add_spell(        spell_id=772,    cooldown=15,                                name="Rend",                icon="ability_gouge.jpg",                         show=False)
WARRIOR_ARMS.add_spell(        spell_id=167105, cooldown=45,  duration=10, color="#ffbf29", name="Colossus Smash",      icon="ability_warrior_colossussmash.jpg",         show=False)
WARRIOR_ARMS.add_spell(        spell_id=118038, cooldown=120, duration=8,                   name="Die by the Sword",    icon="ability_warrior_challange.jpg",             show=False)
WARRIOR_ARMS.add_buff(         spell_id=197690, cooldown=6,                                 name="Defensive Stance",    icon="ability_warrior_defensivestance.jpg",       show=False)

WARRIOR_FURY.add_spell(        spell_id=1719,   cooldown=60,  duration=10,                  name="Recklessness",        icon="warrior_talent_icon_innerrage.jpg")
WARRIOR_FURY.add_spell(        spell_id=184364, cooldown=180, duration=8,                   name="Enraged Regeneration",icon="ability_warrior_focusedrage.jpg",           show=False)
WARRIOR_FURY.add_spell(        spell_id=385059, cooldown=45,  duration=4,  color="#ffbf29", name="Odyn's Fury",         icon="inv_sword_1h_artifactvigfus_d_01.jpg",      show=False)

WARRIOR_PROTECTION.add_spell(  spell_id=385954, cooldown=45,               color="#b34747", name="Shield Charge",       icon="ability_warrior_shieldcharge.jpg",          show=False)
WARRIOR_PROTECTION.add_spell(  spell_id=12975,  cooldown=180, duration=15, color="#ffbf29", name="Last Stand",          icon="spell_holy_ashestoashes.jpg")
WARRIOR_PROTECTION.add_spell(  spell_id=871,    cooldown=120, duration=8,  color="#039dfc", name="Shield Wall",         icon="ability_warrior_shieldwall.jpg")  # CD reduced by Talent per Rage spend
WARRIOR_PROTECTION.add_spell(  spell_id=1160,   cooldown=45,  duration=8,  color="#36b336", name="Demoralizing Shout",  icon="ability_warrior_warcry.jpg", show=False)
WARRIOR_PROTECTION.add_spell(  spell_id=392966, cooldown=90,  duration=30, color="#d1793b", name="Spell Block",         icon="ability_warrior_shieldbreak.jpg", show=False)
