"""RaidZone and Bosses for Patch 10.0 T31: Vault of the Incarnates, first raid tier of Dragonflight."""
# pylint: disable=line-too-long
# pylint: disable=C0326  # spaces

# IMPORT LOCAL LIBRARIES
from lorgs.models.raid_zone import RaidZone

################################################################################################################################################################
#
#   Tier: 30 Vault of the Incarnates
#
################################################################################################################################################################
RAID = RaidZone(id=31, name="Vault of the Incarnates")
VAULT_OF_THE_INCARNATES = RAID


################################################################################
# 01: Eranog
ERANOG = VAULT_OF_THE_INCARNATES.add_boss(id=2587, name="Eranog")

ERANOG.add_cast(
    spell_id=370615, name="Molten Cleave",  # Frontal
    duration=3.5,
    color="#2695d1", icon="ability_rhyolith_magmaflow_wave.jpg"
)

ERANOG.add_cast(
    spell_id=390715, name="Flamerift",  # Adds
    duration=1.5 + 6,
    color="#dbdb2c", icon="inv_misc_head_dragon_01.jpg"
)

ERANOG.add_buff(
    spell_id=370307, name="Collapsing Army",  # Intermission
    color="#46db2c", icon="spell_fire_elemental_totem.jpg"
)


################################################################################
# 02: Terros
TERROS = VAULT_OF_THE_INCARNATES.add_boss(id=2639, name="Terros")

TERROS.add_cast(
    spell_id=376279, name="Concussive Slam", # Tank Slam
    duration=2.5,
    color="#2d82d6", icon="ability_warrior_titansgrip.jpg",
)

TERROS.add_cast(
    spell_id=380487, name="Rock Blast", # Group Soak
    duration=5.5,
    color="#c94949", icon="6bf_blackrock_nova.jpg",
)

TERROS.add_cast(
    spell_id=383073, name="Shattering Impact", # Group Soak
    duration=3.25,
    color="#d6c82d", icon="spell_shaman_earthquake.jpg",
    show=False,
)

TERROS.add_cast(
    spell_id=377166, name="Resonating Annihilation", # Pizza Slice
    duration=6.5,
    color="#2dd635", icon="spell_shaman_improvedfirenova.jpg",
)


################################################################################
# 03: The Primal Council
PRIMAL_COUNCIL = VAULT_OF_THE_INCARNATES.add_boss(id=2590, name="The Primal Council")


################################################################################
# 04: Sennarth, The Cold Breath
SENNARTH = VAULT_OF_THE_INCARNATES.add_boss(id=2592, name="Sennarth, The Cold Breath", nick="Sennarth")


################################################################################
# 05: Dathea, Ascended
DATHEA = VAULT_OF_THE_INCARNATES.add_boss(id=2635, name="Dathea, Ascended", nick="Dathea")

# Tornados
DATHEA.add_cast(
    spell_id=388410, name="Crosswinds", duration=4, show=False,
    color="#6fd1c4", icon="inv_10_jewelcrafting_bg_air.jpg",
)

# Suck in
DATHEA.add_cast(
    spell_id=376943, name="Cyclone", duration=4+10,
    color="#d18726", icon="creatureportrait_cyclone_nodebris.jpg",
)

# Summon Adds
DATHEA.add_cast(
    spell_id=387849, name="Coalescing Storm", duration=5,
    color="#cfcf23", icon="inv_10_elementalspiritfoozles_air.jpg",
)

# Knockback
DATHEA.add_cast(
    spell_id=391382, name="Blowback", duration=4,
    color="#50cc2b", icon="inv_misc_volatileair.jpg",
)

################################################################################
# 06: Kurog Grimtotem
KUROG = VAULT_OF_THE_INCARNATES.add_boss(id=2605, name="Kurog Grimtotem", nick="Kurog")


################################################################################
# 07: Broodkeeper Diurna
DIURNA = VAULT_OF_THE_INCARNATES.add_boss(id=2614, name="Broodkeeper Diurna", nick="Diurna")


################################################################################
# 08: Raszageth the Storm-Eater
RASZAGETH = VAULT_OF_THE_INCARNATES.add_boss(id=2607, name="Raszageth the Storm-Eater", nick="Raszageth")

