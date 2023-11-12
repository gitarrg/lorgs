"""01: Gnarlroot"""

from lorgs.models.raid_boss import RaidBoss


VOLCOROSS = RaidBoss(id=2737, name="Volcoross")
boss = VOLCOROSS


# debuffs
boss.add_cast(
    spell_id=421284,
    name="Coiling Flames",
    duration=1.6,
    color="hsl(270, 60%, 70%)",
    icon="ability_evoker_firestorm.jpg",
)

# group soaks
boss.add_cast(
    spell_id=420933,
    name="Flood of the Firelands",
    duration=5,
    color="#d1c21f",
    icon="spell_shaman_lavasurge.jpg",
)
