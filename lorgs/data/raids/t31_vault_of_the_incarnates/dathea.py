"""05: Dathea, Ascended"""

from lorgs.models.raid_boss import RaidBoss


DATHEA = RaidBoss(id=2635, name="Dathea, Ascended", nick="Dathea")

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
