"""Define the Demon Hunter Class and all its Specs and Spells."""
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
DEMONHUNTER.add_spell(         spell_id=323639, cooldown=90,   duration=6,  color=COL_NF,    name="The Hunt",        icon="ability_ardenweald_demonhunter.jpg")
DEMONHUNTER.add_debuff(        spell_id=317009,                             color=COL_VENTR, name="Sinful Brand",    icon="ability_revendreth_demonhunter.jpg")

DEMONHUNTER_HAVOC.add_spell(   spell_id=200166, cooldown=240,  duration=30, color="#348540", name="Metamorphosis",   icon="ability_demonhunter_metamorphasisdps.jpg")
DEMONHUNTER_HAVOC.add_spell(   spell_id=196718, cooldown=180,  duration=8,                   name="Darkness",        icon="ability_demonhunter_darkness.jpg",          show=False, spell_type=SPELL_TYPE_RAID)
DEMONHUNTER_HAVOC.add_spell(   spell_id=196555, cooldown=180,  duration=5,                   name="Netherwalk",      icon="spell_warlock_demonsoul.jpg",               show=False)

DEMONHUNTER_VENGEANCE.add_spell(spell_id=204021, cooldown=60,  duration=8,  color="#7aeb34", name="Fiery Brand",     icon="ability_demonhunter_fierybrand.jpg")
DEMONHUNTER_VENGEANCE.add_spell(spell_id=212084, cooldown=60,  duration=2,  color="#34ebe1", name="Fel Devastation", icon="ability_demonhunter_feldevastation.jpg",    show=False)
DEMONHUNTER_VENGEANCE.add_spell(spell_id=187827, cooldown=180, duration=15, color="#348540", name="Metamorphosis",   icon="ability_demonhunter_metamorphasistank.jpg")
