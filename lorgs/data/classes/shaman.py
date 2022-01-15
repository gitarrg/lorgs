"""Define the Shaman Class its Specs and Spells."""
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
SHAMAN = WowClass(id=7, name="Shaman", color="#0070DD")

################################################################################
# Specs
#
SHAMAN_ELEMENTAL   = WowSpec(role=RDPS, wow_class=SHAMAN, name="Elemental")
SHAMAN_ENHANCEMENT = WowSpec(role=MDPS, wow_class=SHAMAN, name="Enhancement")
SHAMAN_RESTORATION = WowSpec(role=HEAL, wow_class=SHAMAN, name="Restoration",   short_name="Resto")

################################################################################
# Spells
#
SHAMAN.add_spell(              spell_id=320674, cooldown=90,               color=COL_VENTR, name="Chain Harvest",              icon="ability_revendreth_shaman.jpg",             show=False)
SHAMAN.add_spell(              spell_id=328923, cooldown=120, duration=3,  color=COL_NF,    name="Fae Transfusion",            icon="ability_ardenweald_shaman.jpg",             show=True)
SHAMAN.add_spell(              spell_id=326059, cooldown=45,               color=COL_NECRO, name="Primordial Wave",            icon="ability_maldraxxus_shaman.jpg",             show=False)

SHAMAN.add_spell(              spell_id=21169, name="Reincarnation", icon="spell_shaman_improvedreincarnation.jpg", show=False)

SHAMAN_ELEMENTAL.add_spell(    spell_id=191634, cooldown=60,               color="#00bfff", name="Stormkeeper",                icon="ability_thunderking_lightningwhip.jpg")
SHAMAN_ELEMENTAL.add_spell(    spell_id=198067, cooldown=150, duration=30, color="#ffa500", name="Fire Elemental",             icon="spell_fire_elemental_totem.jpg")
SHAMAN_ELEMENTAL.add_spell(    spell_id=192249, cooldown=150, duration=30, color="#64b8d9", name="Storm Elemental",            icon="inv_stormelemental.jpg")

SHAMAN_ENHANCEMENT.add_spell(  spell_id=114051, cooldown=180,                               name="Ascendance",                 icon="spell_fire_elementaldevastation.jpg")
SHAMAN_ENHANCEMENT.add_spell(  spell_id=51533,  cooldown=120,                               name="Feral Spirit",               icon="spell_shaman_feralspirit.jpg")
SHAMAN_ENHANCEMENT.add_buff(   spell_id=335903, cooldown=60,  duration=12, color="#42bff5", name="Doom Winds",                 icon="ability_ironmaidens_swirlingvortex.jpg")

SHAMAN_RESTORATION.add_spell(  spell_id=108280, cooldown=180, duration=10,                  name="Healing Tide Totem",         icon="ability_shaman_healingtide.jpg")
SHAMAN_RESTORATION.add_spell(  spell_id=98008,  cooldown=180, duration=6,  color="#24b385", name="Spirit Link Totem",          icon="spell_shaman_spiritlink.jpg")
SHAMAN_RESTORATION.add_spell(  spell_id=16191,  cooldown=180, duration=8,  color=COL_MANA,  name="Mana Tide Totem",            icon="spell_frost_summonwaterelemental.jpg",      show=False)
SHAMAN_RESTORATION.add_spell(  spell_id=207399, cooldown=300, duration=30, color="#d15a5a", name="Ancestral Protection Totem", icon="spell_nature_reincarnation.jpg")
SHAMAN_RESTORATION.add_spell(  spell_id=114052, cooldown=180, duration=15,                  name="Ascendance",                 icon="spell_fire_elementaldevastation.jpg")
SHAMAN_RESTORATION.add_spell(  spell_id=198838, cooldown=60, duration=15,  color="#a47ea6", name="Earthen Wall Totem",         icon="spell_nature_stoneskintotem.jpg",           show=False)
SHAMAN_RESTORATION.add_spell(  spell_id=157153, cooldown=30, duration=15,  color="#96d0eb", name="Cloudburst Totem",           icon="ability_shaman_condensationtotem.jpg",      show=False)
