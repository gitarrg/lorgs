"""01: Vexie

Example Fight:
>>> scripts/load_report.py "https://www.warcraftlogs.com/reports/DzLQG1Rkp4xtdJgh?fight=10&type=casts&hostility=1&source=22"

"""

from lorgs.models.raid_boss import RaidBoss


VEXIE = RaidBoss(
    id=3009,
    name="Vexie and the Geargrinders",
    nick="Vexie",
    icon="inv_111_raid_achievement_vexieandthegeargrinders.jpg",
)
boss = VEXIE


################################################################################
# Main Phase


# Spew Oil -> spread
boss.add_cast(
    spell_id=459671,
    name="Spew Oil",
    duration=12,
    color="hsl(170, 60%, 75%)",
    icon="spell_yorsahj_bloodboil_black.jpg",
    show=False,
)

# drop fire puddles -> burn oil
boss.add_cast(
    spell_id=468207,
    name="Incendiary Fire",
    duration=6,
    color="hsl(300, 50%, 50%)",
    icon="spell_shaman_improvedfirenova.jpg",
    show=False,
)

# Exhaust Fumes --> Raid Wide AOE
boss.add_buff(
    spell_id=468149,
    name="Exhaust Fumes",
    duration=6,  # the buff stays but the dmg is only 6sec
    color="hsl(0, 50%, 50%)",
    icon="inv_misc_dust.jpg",
    event_type="applybuff, applybuffstack",
)


# Car Spawns
boss.add_cast(
    spell_id=459943,
    name="Call Bikers",
    duration=1,
    color="hsl(50, 80%, 50%)",
    icon="inv_viciousgoblintrike.jpg",
)


# Tank Buster
boss.add_cast(
    spell_id=459627,
    name="Tank Buster",
    duration=1.5,
    cooldown=25,
    color="#478fb3",
    icon="ability_vehicle_siegeenginecharge.jpg",
    show=False,
)


################################################################################
# Burn Phase

# Tune-Up / Breakdown
boss.add_debuff(
    spell_id=460603,
    name="Mechanical Breakdown",
    color="hsl(120, 70%, 50%)",
    icon="ability_siege_engineer_detonate.jpg",
)
