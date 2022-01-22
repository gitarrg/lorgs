"""Define the Mage Class and all its Specs and Spells."""
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
MAGE = WowClass(id=8, name="Mage", color="#3FC7EB")

################################################################################
# Specs
#
MAGE_ARCANE = WowSpec(role=RDPS, wow_class=MAGE, name="Arcane")
MAGE_FIRE   = WowSpec(role=RDPS, wow_class=MAGE, name="Fire")
MAGE_FROST  = WowSpec(role=RDPS, wow_class=MAGE, name="Frost")

################################################################################
# Spells
#
MAGE.add_spell(        spell_id=314793, cooldown=90,  duration=25, color=COL_VENTR, name="Mirrors of Torment", icon="ability_revendreth_mage.jpg")
MAGE.add_spell(        spell_id=314791, cooldown=60,  duration=3,  color=COL_NF,    name="Shifting Power",     icon="ability_ardenweald_mage.jpg",               show=False)
MAGE.add_spell(        spell_id=307443, cooldown=30,  duration=10, color=COL_KYR,   name="Radiant Spark",      icon="ability_bastion_mage.jpg",                  show=False)
MAGE.add_spell(        spell_id=324220, cooldown=180, duration=25, color=COL_NECRO, name="Deathborne",         icon="ability_maldraxxus_mage.jpg")
MAGE.add_spell(        spell_id=116011, cooldown=45,  duration=12,                  name="Rune of Power",      icon="spell_mage_runeofpower.jpg",                show=False)

MAGE_FIRE.add_spell(   spell_id=190319, cooldown=60,  duration=10, color="#e3b02d", name="Combustion",         icon="spell_fire_sealoffire.jpg",      tags=[TAG_DYNAMIC_CD])
MAGE_FIRE.add_spell(   spell_id=153561, cooldown=45,                                name="Meteor",             icon="spell_mage_meteor.jpg",                     show=False)
MAGE_FIRE.add_buff(    spell_id=333315,                                             name="Sun King's Blessing",icon="ability_mage_firestarter.jpg",              show=True)

MAGE_ARCANE.add_spell( spell_id=12042,  cooldown=100, duration=10,                  name="Arcane Power",       icon="spell_nature_lightning.jpg")  # 2min base cd / reduced by conduit
MAGE_ARCANE.add_spell( spell_id=321507, cooldown=45,  duration=8,                   name="Touch of the Magi",  icon="spell_mage_icenova.jpg")

MAGE_FROST.add_spell(  spell_id=12472,  cooldown=60,  duration=20,                  name="Icy Veins",          icon="spell_frost_coldhearted.jpg",    tags=[TAG_DYNAMIC_CD]) # 3min base cd / reduced by conduit
MAGE_FROST.add_spell(  spell_id=257537, cooldown=45,                                name="Ebonbolt",           icon="artifactability_frostmage_ebonbolt.jpg")
MAGE_FROST.add_spell(  spell_id=84714,  cooldown=60,                                name="Frozen Orb",         icon="spell_frost_frozenorb.jpg")
