"""07: Echo of Neltharion"""

from lorgs.models.raid_boss import RaidBoss


NELTHARION = RaidBoss(id=2684, name="Echo of Neltharion", nick="Neltharion")
boss = NELTHARION

################################################################################
# Phase 1:
# Rushing Shadows ==> random players --> knockback --> breaks wall
boss.add_cast(
    spell_id=407207,
    name="Rushing Darkness",
    duration=5,
    icon="inv_cosmicvoid_missile.jpg",
    color="#3a79f0",
)


# Tank:
# Calamious Strike --> big dropoff aoe circle
#
boss.add_cast(
    spell_id=406222,
    name="Calamitous Strike",
    duration=2,
    icon="inv_sword_138.jpg",
    color="#478fb3",
    show=False,
)


################################################################################
# Phase 2
#

# p2 start?
boss.add_cast(
    spell_id=403057,
    name="Surrender to Corruption",
    duration=10,
    icon="inv_cosmicvoid_debuff.jpg",
    color="#60b336",
)


# Adds Spawn
# Corruption --> corrupteed players break shield
# --> all players kill add

# Tank Hit:
# split soul --> use to break walls
boss.add_cast(
    spell_id=407790,
    name="Sunder Shadow",
    duration=1.5 + 5,  # 1.5sec cast + 5sec debuff
    icon="spell_deathknight_spelldeflection.jpg",
    color="#478fb3",
    show=False,
)


################################################################################
# Phase 3
#

# Rygelon Portals
