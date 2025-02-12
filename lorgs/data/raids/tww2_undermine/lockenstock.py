"""05: Sprocketmonger Lockenstock

PTR Logs:
    Mythic / Northern Sky
    https://www.warcraftlogs.com/reports/YxpKjwFbkrC4VGv3?fight=61


"""

from lorgs.models.raid_boss import RaidBoss


LOCKENSTOCK = RaidBoss(
    id=3013,
    name="Sprocketmonger Lockenstock",
    nick="Lockenstock",
    icon="inv_111_raid_achievement_sprocketmongerlocknstock.jpg",
)
boss = LOCKENSTOCK


# raid wide AoE
boss.add_cast(
    spell_id=465232,
    name="Sonic Ba-Boom",
    duration=2,
    cooldown=10,
    color="hsl(0, 50%, 50%)",
    icon="inv_sonic_debuff.jpg",
)


# Mine spawn / Foot Blasters
# trigger them to explode 1 by 1
# TODO: track triggering
boss.add_cast(
    spell_id=1217231,
    name="Foot-Blasters",
    duration=1.5,
    color="hsl(50, 60%, 50%)",
    icon="inv_10_engineering2_boxofbombs_friendly_color1.jpg",
)


# Zone activation --> move to other side
boss.add_cast(
    spell_id=1218418,
    name="Wire Transfer",
    duration=2,
    color="hsl(210, 50%, 50%)",
    icon="inv_10_engineering_manufacturedparts_electricalparts_color1.jpg",
)


# Drills spawn
boss.add_cast(
    spell_id=1216508,
    name="Screw Up",
    duration=2,
    cooldown=4.5,
    color="hsl(30, 60%, 50%)",
    icon="ability_siege_engineer_sockwave_missile.jpg",
    show=False,
)


# Weapons
boss.add_cast(
    spell_id=465232,
    name="Activate Inventions!",
    duration=1,
    color="hsl(260, 50%, 50%)",
    icon="inv_10_engineering_device_gadget1_color2.jpg",
)

# Rockets
boss.add_cast(
    spell_id=1214872,
    name="Pyro Party Pack",
    duration=1.5,
    color="hsl(280, 60%, 60%)",
    icon="inv_summerfest_groundflower.jpg",
)


# Mythic: Debuffs
boss.add_cast(
    spell_id=1217355,
    name="Polarization Generator",
    duration=4,
    color="hsl(320, 70%, 60%)",
    icon="inv_engineering_90_electrifiedether.jpg",
    show=False,
)

# red lasers


##############
# Intermission / Bleeding Edge
boss.add_cast(
    spell_id=466860,
    name="Bleeding Edge",
    duration=20,
    color="hsl(120, 70%, 50%)",
    icon="spell_yorsahj_bloodboil_purple.jpg",
)
