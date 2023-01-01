"""Define the Demon Hunter Class and all its Specs and Spells."""
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
from lorgs.models.wow_spell import SpellType


################################################################################
# Class
#
DEMONHUNTER  = WowClass(id=12, name="Demon Hunter",  color="#A330C9")

################################################################################
# Specs
#
DEMONHUNTER_HAVOC     = WowSpec(role=MDPS, wow_class=DEMONHUNTER, name="Havoc")
DEMONHUNTER_VENGEANCE = WowSpec(role=TANK, wow_class=DEMONHUNTER, name="Vengeance")

################################################################################
# Spells
#
DEMONHUNTER.add_spell(         spell_id=306830, cooldown=60,                color=COL_KYR,   name="Elysian Decree",  icon="ability_bastion_demonhunter.jpg",           show=False)
DEMONHUNTER.add_spell(         spell_id=370966, cooldown=90,   duration=6,  color="#2075d6", name="The Hunt",        icon="ability_ardenweald_demonhunter.jpg")
DEMONHUNTER.add_spell(         spell_id=196718, cooldown=180,  duration=8,                   name="Darkness",        icon="ability_demonhunter_darkness.jpg",          show=False, spell_type=SpellType.RAID)
DEMONHUNTER.add_spell(         spell_id=198793, cooldown=25,                color="#c95bcf", name="Vengeful Retreat", icon="ability_demonhunter_vengefulretreat2.jpg", show=False)

DEMONHUNTER_HAVOC.add_spell(   spell_id=198589, cooldown=60,   duration=10,                  name="Blur",            icon="ability_demonhunter_blur.jpg", show=False)
DEMONHUNTER_HAVOC.add_spell(   spell_id=258860, cooldown=40,   duration=4,  color="#9177fc", name="Essence Break",   icon="spell_shadow_ritualofsacrifice.jpg",               show=False)
DEMONHUNTER_HAVOC.add_spell(   spell_id=200166, cooldown=240,  duration=30, color="#348540", name="Metamorphosis",   icon="ability_demonhunter_metamorphasisdps.jpg")

DEMONHUNTER_VENGEANCE.add_spell(spell_id=204021, cooldown=60,  duration=8,  color="#7aeb34", name="Fiery Brand",     icon="ability_demonhunter_fierybrand.jpg")
DEMONHUNTER_VENGEANCE.add_spell(spell_id=212084, cooldown=60,  duration=2,  color="#34ebe1", name="Fel Devastation", icon="ability_demonhunter_feldevastation.jpg",    show=False)
DEMONHUNTER_VENGEANCE.add_spell(spell_id=187827, cooldown=180, duration=15, color="#348540", name="Metamorphosis",   icon="ability_demonhunter_metamorphasistank.jpg")
DEMONHUNTER_VENGEANCE.add_debuff(spell_id=209261, cooldown=480, duration=15, color="#348540", name="Last Resort",   icon="inv_glaive_1h_artifactaldorchi_d_06.jpg")
