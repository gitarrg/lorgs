"""01: Gnarlroot"""

from lorgs.models.raid_boss import RaidBoss


FYRAKK = RaidBoss(id=2677, name="Fyrakk the Blazing", nick="Fyrakk")
boss = FYRAKK


boss.add_cast(
    spell_id=421455,
    name="Burning Scales",
    duration=10,
    color="hsl(30, 50%, 50%)",
    icon="inv_10_skinning_scales_red.jpg",
)


boss.add_cast(
    spell_id=419123,
    name="Flamefall",
    duration=5,
    color="hsl(300, 30%, 50%)",
    icon="spell_shaman_stormearthfire.jpg",
)


# Small puddles --> drop and move
# Dream Rend: big AOE
# Blze: Move out


################################################################################
# Intermission 1 ' 70%
# - soak orbs

# Corrupt: Break Shield + Heal


################################################################################
# Phase 2

# Heal small Adds

# Big Breath --> Dodge + kill Adds
# Landing: big DMG


################################################################################
# Phase 3

# Appocalypse Roar = one shot
# pickup seeds to get biggus shildus
boss.add_cast(
    spell_id=422837,
    name="Apocalypse Roar",
    duration=12,
    color="hsl(0, 50%, 50%)",
    icon="inv_misc_head_dragon_red.jpg",
)


boss.add_cast(
    spell_id=425492,
    name="Infernal Maw",
    duration=1,
    color="#478fb3",
    icon="ability_physical_taunt.jpg",
    show=False,
)
