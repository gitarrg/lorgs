"""Define the Rogue Class and all its Specs and Spells."""
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
ROGUE = WowClass(id=4, name="Rogue", color="#FFF468")

################################################################################
# Specs
#
ROGUE_ASSASSINATION = WowSpec(role=MDPS, wow_class=ROGUE, name="Assassination", short_name="Assa")
ROGUE_OUTLAW        = WowSpec(role=MDPS, wow_class=ROGUE, name="Outlaw")
ROGUE_SUBTLETY      = WowSpec(role=MDPS, wow_class=ROGUE, name="Subtlety")

################################################################################
# Spells
#
ROGUE.add_spell(               spell_id=1856,   cooldown=120,              color="#999999", name="Vanish",              icon="ability_vanish.jpg",                       show=False)
ROGUE.add_spell(               spell_id=323547, cooldown=45, duration=45,  color=COL_KYR,   name="Echoing Reprimand",   icon="ability_bastion_rogue.jpg",                show=False)
ROGUE.add_spell(               spell_id=323654, cooldown=90, duration=12,  color=COL_VENTR, name="Flagellation",        icon="ability_revendreth_rogue.jpg",             show=False)
ROGUE.add_spell(               spell_id=328547, cooldown=30,               color=COL_NECRO, name="Serrated Bone Spike", icon="ability_maldraxxus_rogue.jpg",             show=False)
ROGUE.add_spell(               spell_id=328305, cooldown=90,               color=COL_NF,    name="Sepsis",              icon="ability_ardenweald_rogue.jpg",             show=False)

ROGUE.add_spell(               spell_id=31224,  cooldown=60,  duration=5,                   name="Cloak of Shadows",    icon="spell_shadow_nethercloak.jpg",             show=False)
ROGUE.add_buff(                spell_id=45182,  cooldown=360, duration=3,                   name="Cheating Death",      icon="ability_rogue_cheatdeath.jpg",             show=False)
ROGUE.add_spell(               spell_id=5277,   cooldown=120, duration=10,                  name="Evasion",             icon="spell_shadow_shadowward.jpg",              show=False)
ROGUE.add_spell(               spell_id=185311, cooldown=30,  duration=4,                   name="Crimson Vial",        icon="ability_rogue_crimsonvial.jpg",            show=False)
ROGUE.add_spell(               spell_id=1966,   cooldown=15,  duration=6,                   name="Feint",               icon="ability_rogue_feint.jpg",                  show=False)

ROGUE_ASSASSINATION.add_spell( spell_id=703,    cooldown=6,   duration=18,                  name="Garrote",             icon="ability_rogue_garrote.jpg",                show=False)
ROGUE_ASSASSINATION.add_spell( spell_id=1943,                                               name="Rupture",             icon="ability_rogue_rupture.jpg",                show=False)
ROGUE_ASSASSINATION.add_spell( spell_id=121411,                                             name="Crimson Tempest",     icon="inv_knife_1h_cataclysm_c_05.jpg",          show=False)
ROGUE_ASSASSINATION.add_spell( spell_id=5938,   cooldown=25,                                name="Shiv",                icon="inv_throwingknife_04.jpg",                 show=False)
ROGUE_ASSASSINATION.add_spell( spell_id=79140,  cooldown=120, duration=20, color="#bf291f", name="Vendetta",            icon="ability_rogue_deadliness.jpg")

ROGUE_SUBTLETY.add_spell(      spell_id=121471, cooldown=180, duration=20, color="#9a1be3", name="Shadow Blades",       icon="inv_knife_1h_grimbatolraid_d_03.jpg")
ROGUE_SUBTLETY.add_spell(      spell_id=5171,                                               name="Slice and Dice",      icon="ability_rogue_slicedice.jpg")
ROGUE_SUBTLETY.add_spell(      spell_id=185313, cooldown=0,   duration=8,  color="#cf5dab", name="Shadow Dance",        icon="ability_rogue_shadowdance.jpg",            show=False)
ROGUE_SUBTLETY.add_spell(      spell_id=212283, cooldown=30,  duration=10,                  name="Symbols of Death",    icon="spell_shadow_rune.jpg")

ROGUE_OUTLAW.add_spell(        spell_id=315508,               duration=30, color="#c7813c", name="Roll the Bones",      icon="ability_rogue_rollthebones.jpg",           show=False)
ROGUE_OUTLAW.add_spell(        spell_id=271877, cooldown=0,                                 name="Blade Rush",          icon="ability_arakkoa_spinning_blade.jpg",       show=False)
ROGUE_OUTLAW.add_spell(        spell_id=13750,  cooldown=0,   duration=20,                  name="Adrenaline Rush",     icon="spell_shadow_shadowworddominate.jpg")
