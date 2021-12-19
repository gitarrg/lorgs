"""Define the Warlock Class its Specs and Spells."""
# pylint: disable=line-too-long
# pylint: disable=bad-whitespace
# pylint: disable=wildcard-import
# pylint: disable=unused-wildcard-import

# IMPORT LOCAL LIBRARIES
from lorgs.data.constants import *
from lorgs.data.roles import *
from lorgs.models.wow_class import WowClass
from lorgs.models.wow_spec import WowSpec
from lorgs.models.wow_spell import WowSpell


################################################################################
# Class
#
WARLOCK = WowClass(id=9, name="Warlock", color="#8788EE")

################################################################################
# Specs
#
WARLOCK_AFFLICTION  = WowSpec(role=RDPS, wow_class=WARLOCK, name="Affliction",  short_name="Aff")
WARLOCK_DEMONOLOGY  = WowSpec(role=RDPS, wow_class=WARLOCK, name="Demonology",  short_name="Demo")
WARLOCK_DESTRUCTION = WowSpec(role=RDPS, wow_class=WARLOCK, name="Destruction", short_name="Destro")

################################################################################
# Spells
#
WARLOCK.add_spell(             spell_id=325640, cooldown=60,  duration=8,  color=COL_NF,    name="Soul Rot",               icon="ability_ardenweald_warlock.jpg", show=False)

WARLOCK_AFFLICTION.add_spell(  spell_id=205180, cooldown=180, duration=8,  color="#49ad6e", name="Summon Darkglare",       icon="inv_beholderwarlock.jpg")
WARLOCK_AFFLICTION.add_spell(  spell_id=113860, cooldown=120, duration=20, color="#c35ec4", name="Dark Soul: Misery",      icon="spell_warlock_soulburn.jpg")
WARLOCK_AFFLICTION.add_spell(  spell_id=205179, cooldown=45,  duration=16, color="#7833b0", name="Phantom Singularity",    icon="inv_enchant_voidsphere.jpg")

WARLOCK_DEMONOLOGY.add_spell(  spell_id=265187, cooldown=60,  duration=15, color="#9150ad", name="Summon Demonic Tyrant",  icon="inv_summondemonictyrant.jpg", tags=[TAG_DYNAMIC_CD])
WARLOCK_DEMONOLOGY.add_spell(  spell_id=111898, cooldown=120, duration=17, color="#c46837", name="Grimoire: Felguard",     icon="spell_shadow_summonfelguard.jpg")
WARLOCK_DEMONOLOGY.add_spell(  spell_id=264119, cooldown=45,  duration=15, color="#69b851", name="Summon Vilefiend",       icon="inv_argusfelstalkermount.jpg")
WARLOCK_DEMONOLOGY.add_spell(  spell_id=267217, cooldown=180, duration=15,                  name="Nether Portal",          icon="inv_netherportal.jpg")

WARLOCK_DESTRUCTION.add_spell( spell_id=1122,   cooldown=180, duration=30, color="#91c45a", name="Summon Infernal",        icon="spell_shadow_summoninfernal.jpg")
WARLOCK_DESTRUCTION.add_spell( spell_id=113858, cooldown=120, duration=20, color="#c35ec4", name="Dark Soul: Instability", icon="spell_warlock_soulburn.jpg")

# Additional Spells (not tracked)
SOULSTONE_RESURRECTION = WowSpell(spell_id=95750, name="Soulstone", icon="spell_shadow_soulgem.jpg")
