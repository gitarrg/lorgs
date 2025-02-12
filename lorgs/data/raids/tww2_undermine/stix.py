"""04: Stix Bunkjunker


PTR Logs:
    Heroic / Melee Mechanics
    https://www.warcraftlogs.com/reports/jMwdH1rf3XZK7Avp?fight=7

"""

from lorgs.models.raid_boss import RaidBoss


STIX = RaidBoss(
    id=3012,
    name="Stix Bunkjunker",
    nick="Stix",
    icon="inv_111_raid_achievement_stixbunkjunker.jpg",
)
boss = STIX


#### Phase 1:

# Electromagnetic Sorting =
# - tank + random players transform into balls
#   - soak small -> medium -> large trash to grow
# - spawns adds + bombs
boss.add_cast(
    spell_id=464399,
    name="Electromagnetic Sorting",
    duration=1,
    cooldown=5,
    color="hsl(0, 50%, 50%)",
    icon="inv_10_engineering_manufacturedparts_mechanicalparts_color3.jpg",
)


# Incinerator = red spread circles on random players
# https://www.wowhead.com/ptr-2/spell=464149/incinerator
boss.add_cast(
    spell_id=464149,
    name="Incinerator",
    duration=3,
    color="hsl(35, 75%,50%)",
    icon="ability_ironmaidens_bombardment.jpg",
    show=False,
)


# Tank Hit: Demolish
# https://www.wowhead.com/ptr-2/spell=464112/demolish
boss.add_cast(
    spell_id=464112,
    name="Demolish",
    duration=1.25,
    cooldown=50,
    color="#478fb3",
    icon="inv_misc_enggizmos_12.jpg",
    show=False,
)

# Tank Hit: Meltdown
# https://www.wowhead.com/ptr-2/spell=1217954/meltdown'
boss.add_cast(
    spell_id=1217954,
    name="Meltdown",
    duration=1,
    cooldown=3,
    color="##3fbfbd",
    icon="inv_misc_enggizmos_15.jpg",
    show=False,
)


# Intermission
boss.add_cast(
    spell_id=467117,
    name="Overdrive / Trash Compactor",
    duration=10,  # aprox duration
    color="hsl(120, 70%, 50%)",
    icon="spell_nature_unrelentingstorm.jpg",
)
