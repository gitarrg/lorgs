"""02: Terros."""

from lorgs.models.raid_boss import RaidBoss


TERROS = RaidBoss(
    id=2639,
    name="Terros",
    icon="achievement_raidprimalist_terros.jpg",
)

TERROS.add_cast(
    spell_id=376279,
    name="Concussive Slam",  # Tank Slam
    duration=2.5,
    color="#2d82d6",
    icon="ability_warrior_titansgrip.jpg",
)

TERROS.add_cast(
    spell_id=380487,
    name="Rock Blast",  # Group Soak
    duration=5.5,
    color="#c94949",
    icon="6bf_blackrock_nova.jpg",
)

TERROS.add_cast(
    spell_id=383073,
    name="Shattering Impact",  # Group Soak
    duration=3.25,
    color="#d6c82d",
    icon="spell_shaman_earthquake.jpg",
    show=False,
)

TERROS.add_cast(
    spell_id=377166,
    name="Resonating Annihilation",  # Pizza Slice
    duration=6.5,
    color="#2dd635",
    icon="spell_shaman_improvedfirenova.jpg",
)

TERROS.add_cast(
    spell_id=396351,
    name="Infused Fallout",  # Mythic Debuff
    duration=2,
    color="#9e4ecc",
    icon="spell_quicksand.jpg",
)
