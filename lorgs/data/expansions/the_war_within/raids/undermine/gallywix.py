"""08: Chrome King Gallywix"""

from lorgs.data.classes import *
from lorgs.models.raid_boss import RaidBoss


GALLYWIX = RaidBoss(
    id=3016,
    name="Chrome King Gallywix",
    nick="Gallywix",
    icon="inv_111_raid_achievement_chromekinggallywix.jpg",
)
boss = GALLYWIX


################################################################################
# Trinkets

CHROMEBUSTIBLE_BOMB_SUIT = GALLYWIX.add_trinket(
    spell_id=466810,  # Spell and Buff ID
    cooldown=90,
    duration=20,  # 20sec or until shield consumed
    name="Chromebustible Bomb Suit",
    icon="inv_111_bombsuit_gallywix.jpg",
    item=230029,
)
"""On Use dmg reduction

> Use: Rapidly deploy the bomb suit to reduce damage taken by 75% for 20 sec or until
> 6290790 damage has been prevented.
> Upon depletion, the bomb suit detonates to deal 441294 Fire damage split between
> nearby enemies. (1 Min, 30 Sec Cooldown)
"""
CHROMEBUSTIBLE_BOMB_SUIT.add_specs(*TANK.specs)


EYE_OF_KEZAN = GALLYWIX.add_trinket(
    spell_id=0,
    cooldown=0,
    name="Eye of Kezan",
    icon="spell_azerite_essence08.jpg",
    item=230198,
)
"""Mastery + Main Stat Proc

> Equip: Your spells and abilities have a high chance to empower the Eye and
> grant you 284 <Primary Stat> up to 20 times, decaying rapidly upon leaving combat.
> While fully empowered, the Eye instead deals 64528 Fire damage to enemies or heals allies for 96796.
"""
