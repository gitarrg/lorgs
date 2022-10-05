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
RED_1 = "#bf3030" # hsv(0, 0.75, 0.75)

KUROG = VAULT_OF_THE_INCARNATES.add_boss(id=2605, name="Kurog Grimtotem", nick="Kurog")

# Intermission
KUROG.add_buff(spell_id=374779, name="Primal Barrier", color="#30bf30", icon="inv_10_elementalcombinedfoozles_primordial.jpg")

# Fire
KUROG.add_cast(spell_id=382563, name="Magma Burst", duration=1.5 + 10, color="#FFF", icon="ability_rhyolith_magmaflow_wave.jpg")
KUROG.add_cast(spell_id=374022, name="Searing Carnage", duration=3 + 5, color=RED_1, icon="spell_fire_moltenblood.jpg")

# Frost
KUROG.add_cast(spell_id=373678, name="Biting Chill", duration=10, color="#63c4c9", icon="spell_frost_arcticwinds.jpg")
KUROG.add_cast(spell_id=391019, name="Frigid Torrent", duration=2+4, color="#63c4c9", icon="spell_frost_ring-of-frost.jpg", show=False)
KUROG.add_cast(spell_id=372456, name="Absolute Zero", duration=2+6, color=RED_1, icon="spell_frost_glacier.jpg")

# Earth
KUROG.add_cast(spell_id=390796, name="Erupting Bedrock", duration=5, color="#bf8330", icon="spell_shaman_earthquake.jpg", show=False)
KUROG.add_cast(spell_id=391055, name="Enveloping Earth", duration=1.5, color="#bf8330", icon="inv_elementalearth2.jpg")
KUROG.add_cast(spell_id=374691, name="Seismic Rupture", duration=5, color=RED_1, icon="spell_nature_earthquake.jpg")

# Storm
KUROG.add_cast(spell_id=390920, name="Shocking Burst", duration=5, color="#30bfa0", icon="spell_nature_unrelentingstorm.jpg")
KUROG.add_cast(spell_id=373487, name="Lightning Crash", duration=5, color="#30bfa0", icon="spell_shaman_crashlightning.jpg")
KUROG.add_cast(spell_id=374215, name="Thunder Strike", duration=7, color=RED_1, icon="ability_vehicle_electrocharge.jpg")


################################################################################
# 07: Broodkeeper Diurna
DIURNA = VAULT_OF_THE_INCARNATES.add_boss(id=2614, name="Broodkeeper Diurna", nick="Diurna")


################################################################################
# 08: Raszageth the Storm-Eater
RASZAGETH = VAULT_OF_THE_INCARNATES.add_boss(id=2607, name="Raszageth the Storm-Eater", nick="Raszageth")

