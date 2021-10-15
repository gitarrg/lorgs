"""Define the Monk Class and all its Specs and Spells."""
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
MONK = WowClass(id=10, name="Monk", color="#00FF98")

################################################################################
# Specs
#
MONK_BREWMASTER = WowSpec(role=TANK, wow_class=MONK, name="Brewmaster")
MONK_MISTWEAVER = WowSpec(role=HEAL, wow_class=MONK, name="Mistweaver")
MONK_WINDWALKER = WowSpec(role=MDPS, wow_class=MONK, name="Windwalker")

################################################################################
# Spells
#
MONK.add_spell(           spell_id=310454, cooldown=120, duration=30, color=COL_KYR,   name="Weapons of Order",                icon="ability_bastion_monk.jpg",            show=False)
MONK.add_spell(           spell_id=325216, cooldown=60,  duration=10, color=COL_NECRO, name="Bonedust Brew",                   icon="ability_maldraxxus_monk.jpg",         show=False)
MONK.add_spell(           spell_id=326860, cooldown=180, duration=24, color=COL_VENTR, name="Fallen Order",                    icon="ability_revendreth_monk.jpg",         show=True)
MONK.add_spell(           spell_id=327104, cooldown=30,  duration=30, color=COL_NF,    name="Faeline Stomp",                   icon="ability_ardenweald_monk.jpg",         show=False)
MONK.add_spell(           spell_id=322109, cooldown=180,              color="#c72649", name="Touch of Death",                  icon="ability_monk_touchofdeath.jpg")

MONK_MISTWEAVER.add_spell(spell_id=322118, cooldown=180, duration=3.5,                 name="Invoke Yu'lon, the Jade Serpent", icon="ability_monk_dragonkick.jpg")
MONK_MISTWEAVER.add_spell(spell_id=115310, cooldown=180,              color="#00FF98", name="Revival",                         icon="spell_monk_revival.jpg")
MONK_MISTWEAVER.add_spell(spell_id=325197, cooldown=180, duration=25, color="#e0bb36", name="Invoke Chi-Ji, the Red Crane",    icon="inv_pet_cranegod.jpg")

MONK_WINDWALKER.add_spell(spell_id=123904, cooldown=120, duration=24, color="#8cdbbc", name="Invoke Xuen, the White Tiger",    icon="ability_monk_summontigerstatue.jpg")
MONK_WINDWALKER.add_spell(spell_id=137639, cooldown=90,  duration=15, color="#be53db", name="Storm, Earth, and Fire",          icon="spell_nature_giftofthewild.jpg")

MONK_BREWMASTER.add_spell(spell_id=322507, cooldown=60,  duration=0,  color="#45f9ff", name="Celestial Brew",                  icon="ability_monk_ironskinbrew.jpg",        show=False)
MONK_BREWMASTER.add_spell(spell_id=132578, cooldown=105, duration=25,                  name="Invoke Niuzao the Black Ox",      icon="spell_monk_brewmaster_spec.jpg",       tags=[TAG_DYNAMIC_CD])  # base cd =3min / reduced with conduit
MONK_BREWMASTER.add_spell(spell_id=122278, cooldown=120, duration=10, color="#fcba03", name="Dampen Harm",                     icon="ability_monk_dampenharm.jpg")
MONK_BREWMASTER.add_spell(spell_id=115176, cooldown=300, duration=8,                   name="Zen Meditation",                  icon="ability_monk_zenmeditation.jpg")
MONK_BREWMASTER.add_spell(spell_id=115203, cooldown=360, duration=15, color="#ffb145", name="Fortifying Brew",                 icon="ability_monk_fortifyingale_new.jpg")
