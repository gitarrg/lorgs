"""04: Sennarth, The Cold Breath"""

from lorgs.models.raid_boss import RaidBoss


SENNARTH = RaidBoss(id=2592, name="Sennarth, The Cold Breath", nick="Sennarth")


##############
# P1

# Spiders
SENNARTH.add_cast(
    spell_id=372238, name="Call Spiderlings", duration=9,
    color="#60bf30", icon="inv_misc_monsterspidercarapace_01.jpg",
)

# Web
SENNARTH.add_cast(
    spell_id=372082, name="Enveloping Webs", duration=1+6,
    show=False,
    color="#9060bf", icon="inv_misc_web_01.jpg",
)


SENNARTH.add_cast(
    spell_id=373405, name="Gossamer Burst", duration=3+6,
    color="#ffd500", icon="priest_icon_chakra.jpg",
)


##############
# P2

# Enrage
SENNARTH.add_cast(
    spell_id=372648, name="Pervasive Cold", duration=6,
    color="#bf3030", icon="ability_mage_chilledtothebone.jpg",
)

# Knockback
SENNARTH.add_cast(
    spell_id=373027, name="Suffocating Webs", duration=3+6,
    color="#af60bf", icon="inv_misc_web_02.jpg",
)
