"""03: Rik

Example PTR Logs:
    * Mythic / Northern Sky:
      https://www.warcraftlogs.com/reports/9FCGxtgrqwM1h2AH?fight=23

"""

from lorgs.models.raid_boss import RaidBoss


RIK = RaidBoss(
    id=3011,
    name="Rik Reverb",
    nick="Rik",
    icon="inv_111_raid_achievement_rikreverb.jpg",
)
boss = RIK

################################################################################
# Phase 1

# Amplification
# - shoots out waves (2 his = MC)
# - click to drain energy
# - Mythic:
#   - spawn with shield
#   - requires 2 players with "Faulty Zap / Blue Circles" to "egg break" the shield
boss.add_cast(
    spell_id=473748,
    name="Amplification!",
    duration=3.3,
    color="hsl(0, 50%, 50%)",
    icon="inv_gizmo_goblinboombox_01.jpg",
)


# https://www.wowhead.com/ptr-2/spell=466866/echoing-chant
# 3.5sec Cast
# Rik rally-chants about Chrome-King Gallywix causing Resonant Echoes to burst out from all amplifiers in random directions.
# icon="ability_warrior_battleshout.jpg"


# Sound Canon = Blue Beam
# - Mythic: soak with multiple players
boss.add_cast(
    spell_id=467606,
    name="Sound Cannon",
    duration=5,
    color="hsl(220, 50%, 50%)",
    icon="inv_sonic_orb.jpg",
)


# Faulty Zap = Spread Blue Circles
boss.add_cast(
    spell_id=466961,  # +466979
    name="Faulty Zap",
    duration=2.125,
    cooldown=12,  # debuff
    color="hsl(180, 50%, 50%)",
    icon="ability_thunderking_overcharge.jpg",
    show=False,
)

# Sparkblast Ignition = Adds
# - gives buff when hitting them
# - explode when killed (2 explosion at same time = wipe)


################################################################################
# Intermission

# Intermission Cast / Buff
# tbd: do we track the cast or only buff?
boss.add_cast(
    spell_id=464584,  # buff: 1213817
    name="Sound Cloud",
    duration=5 + 32,  # 5sec Cast + 32sec Duration
    color="hsl(120, 70%, 50%)",
    icon="ability_vehicle_shellshieldgenerator_green.jpg",
)

# run to activated amplifier and click to channel into it
# big wave knocks everyone up + actives another pillar
boss.add_cast(
    spell_id=473260,  # buff: 1213817
    name="Blaring Drop",
    duration=5,
    color="hsl(300, 75%, 75%)",
    icon="ability_socererking_forcenova.jpg",
    show=False,
)
