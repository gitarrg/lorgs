"""06: One-Armed Bandit

PTR Logs:
    Mythic / Northern Sky:
    https://www.warcraftlogs.com/reports/YxpKjwFbkrC4VGv3?fight=71&type=casts&hostility=1
"""

from lorgs.models.raid_boss import RaidBoss


ONE_ARMED_BANDIT = RaidBoss(
    id=3014,
    name="One-Armed Bandit",
    nick="Bandit",
    icon="inv_111_raid_achievement_onearmedbandit.jpg",
)
boss = ONE_ARMED_BANDIT


# Pay-line
boss.add_cast(
    spell_id=460181,
    name="Pay-Line",
    duration=1 + 3,
    color="hsl(40, 70%, 50%)",
    icon="inv_10_fishing_dragonislescoins_gold.jpg",
    show=False,
)

# Heal Absorb / Vile Exhaust
boss.add_cast(
    spell_id=469993,
    name="Foul Exhaust",
    duration=5,  # not real duration
    color="hsl(280, 75%, 60%)",
    icon="inv_elemental_mote_shadow01.jpg",
)

# Tank Hit: "The Big Hit"
# Mythic = 2 Circles
boss.add_cast(
    spell_id=460472,
    name="The Big Hit",
    duration=2.5,
    cooldown=30,
    color="#478fb3",
    icon="ability_warrior_decisivestrike.jpg",
    show=False,
)


# Spin to Win = Adds
# - spawns 3/4 Adds
# - kill 2 --> pickup item and deposit to boss
# -> combination of items deposited determines next mechanic
boss.add_cast(
    spell_id=461060,
    name="Spin To Win!",
    duration=2,
    cooldown=30,
    color="hsl(120, 50%, 50%)",
    icon="achievement_battleground_templeofkotmogu_02.jpg",
)


# Rewards
rewards = boss.add_cast(
    spell_id=464772,
    name="Reward",
    duration=10,  # idk
    color="hsl(100, 70%, 50%)",
    icon="ability_mage_fierypayback.jpg",
    variations=[
        464772,  # Reward: Shock and Flame
        464801,  # Reward: Shock and Bomb
        464804,  # Reward: Flame and Bomb
        464806,  # Reward: Flame and Coin
        464809,  # Reward: Coin and Shock
        464810,  # Reward: Coin and Bomb
    ],
)

# todo: implement something like this?
# rewards.add_variation(spell_id=464772, name="Reward: Shock and Flame", icon="ability_mage_fierypayback.jpg")
# rewards.add_variation(spell_id=464801, name="Reward: Shock and Bomb", icon="inv_eng_bombicestun.jpg")
# rewards.add_variation(spell_id=464804, name="Reward: Flame and Bomb", icon="inv_eng_bombfire.jpg")
# rewards.add_variation(spell_id=464806, name="Reward: Flame and Coin", icon="ability_creature_cursed_01.jpg")
# rewards.add_variation(spell_id=464809, name="Reward: Coin and Shock", icon="inv_misc_enggizmos_13.jpg")
# rewards.add_variation(spell_id=464810, name="Reward: Coin and Bomb", icon="inv_misc_bomb_04.jpg")


#################################################
### Phase 2
