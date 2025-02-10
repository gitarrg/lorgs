"""02: Cauldron of Carnage


>>> scripts/load_report.py "https://www.warcraftlogs.com/reports/DzLQG1Rkp4xtdJgh?fight=16"

"""

from lorgs.models.raid_boss import RaidBoss


CAULDRON = RaidBoss(
    id=3010,
    name="Cauldron of Carnage",
    nick="Cauldron",
    icon="inv_11_arenaboss_colossalclash.jpg",
)
boss = CAULDRON


################################################################################
# Torq

# small adds
# Voltaic Image

# Pools
boss.add_cast(
    spell_id=463900,
    name="Thunderdrum Salvo",
    duration=8,
    color="hsl(170, 75%, 60%)",
    icon="inv_11_arenaboss_thunderdrumsalvo.jpg",
)

# Tank Hit
boss.add_cast(
    spell_id=463798,
    name="Lightning Bash",
    duration=4,  # not sure how long the combo lasts
    color="#478fb3",
    icon="inv_gizmo_supersappercharge.jpg",
    show=False,
)


################################################################################
# Flarendo


# Group Soak
boss.add_cast(
    spell_id=473650,
    name="Scrapbomb",
    duration=10,
    color="hsl(20, 75%, 60%)",
    icon="inv_10_engineering2_boxofbombs_friendly_color1.jpg",
)

# Beam
boss.add_cast(
    spell_id=472233,
    name="Blastburn Roarcannon",
    duration=3.5,
    cooldown=3,
    color="hsl(40, 75%, 60%)",
    icon="spell_shaman_shockinglava.jpg",
)

# Tank hit
boss.add_cast(
    spell_id=1214190,
    name="Eruption Stomp",
    duration=4,
    color="#478fb3",
    icon="inv_gizmo_supersappercharge.jpg",
    show=False,
)

# Spread
# Molten Phlem


################################################################################
# 100% Energy -> (Intermission)

boss.add_buff(
    spell_id=465872,
    name="Colossal Clash",
    duration=20,
    color="hsl(120, 70%, 50%)",
    icon="inv_11_arenaboss_colossalclash.jpg",
)
