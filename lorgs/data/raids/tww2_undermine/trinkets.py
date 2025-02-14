from lorgs.data.classes import *
from lorgs.models.wow_trinket import WowTrinket


class UndermineTrinket(WowTrinket):
    """Trinket which drops in the 11.1 Raid: Liberation of Undermine."""

    ilvl: int = 662
    query: bool = True
    color: str = "#a335ee"


################################################################################
# Vexie


GEARGRINDERS_SPARE_KEYS = UndermineTrinket(
    spell_id=0,  # TODO: on PTR the trinket's cast did not show up in logs
    cooldown=120,
    name="Geargrinder's Spare Keys",
    icon="inv_111_goblintrikekeychain_gallywix.jpg",
    item=230197,
)
"""On-Use DMG

> Use: Launch a Geargrinder trike to its final blaze of glory, exploding upon impacting
> the first enemy in its path to deal 1320420 Fire damage split between all nearby enemies. (2 Min Cooldown)
"""
GEARGRINDERS_SPARE_KEYS.add_specs(*ALL_SPECS)


VEXIES_PIT_WHISTLE = UndermineTrinket(
    spell_id=466652,
    duration=5,
    cooldown=90,
    name="Vexie's Pit Whistle",
    icon="inv_111_sapper_bilgewater.jpg",
    item=230019,
)
"""Summon Pet which explodes after 5sec

> Use: Summon Pitbot Geardo to assist you for 5 sec, coating nearby enemies
> with rancid motor oil for additional threat. Geardo ensures you take the blame.
>
> Geardo departs explosively to deal 582636 Fire damage split between nearby enemies,
> increased by 15% if recently oiled. (500ms cooldown) (1 Min, 30 Sec Cooldown)

"""
VEXIES_PIT_WHISTLE.add_specs(*STR_SPECS)
VEXIES_PIT_WHISTLE.add_specs(*AGI_SPECS)


################################################################################
# Cauldron of Carnage


FLARENDOS_PILOT_LIGHT = UndermineTrinket(
    spell_id=471142,
    cooldown=120,
    duration=15,
    name="Flarendo's Pilot Light",
    icon="inv_111_flarendosflame_gallywix.jpg",
    item=230191,
)
"""On-Use Int for 15sec + dmg after 3 harmful spells

> Use: Reignite the pilot light to gain 6712 Intellect for 15 sec.
> After casting 3 harmful spells, it unleashes a beam dealing 1664237 Fire damage
> to your primary target and 133138.96 damage to up to 5 enemies in its path. (2 Min Cooldown)
"""
FLARENDOS_PILOT_LIGHT.add_specs(*INT_SPECS)


TORQS_BIG_RED_BUTTON = UndermineTrinket(
    spell_id=470286,
    cooldown=120,
    duration=15,
    name="Torq's Big Red Button",
    icon="inv_111_redbutton_bilgewater.jpg",
    item=230190,
)
"""On-use Strength + dmg after 3 harmful spells, increasing on each use.

> Use: Unleash your inner tempest to gain 6712 Strength for 15 sec.
> Your next 3 abilities cause a lightning blast dealing [(299563 * 0.66 0.66 1)]
> Nature damage to your primary target. Damage increased by 100% with each subsequent blast. (2 Min Cooldown)

"""
TORQS_BIG_RED_BUTTON.add_specs(*STR_SPECS)


################################################################################
# Rik Reverb


REVERB_RADIO = UndermineTrinket(
    spell_id=0,
    duration=15,
    name="Reverb Radio",
    icon="inv_111_statsoundwaveemitter_blackwater.jpg",
    item=230194,
)
"""Stacking Buff + Bigger VBuff at 5 Stacks

> Your spells and abilities have a high chance to Hype you up, granting 314 Haste up to 5 times.
> Upon reaching maximum Hype, amp it up by 100% for 15 sec before starting again.
"""
# REVERB_RADIO.add_specs(*ALL_SPECS)


################################################################################
# Stix Bunkjunker


JUNKMAESTROS_MEGA_MAGNET = UndermineTrinket(
    spell_id=471212,
    duration=6,
    cooldown=20,
    name="Junkmaestro's Mega Magnet",
    icon="inv_111_magnet_gallywix.jpg",
    item=230189,
)
"""Collect stacks -> consume them for on-use dmg

Buff: 1219661

> Equip: Your damaging abilities have a very high chance to charge the magnet, up to 30 times.
> Use: Reverse the magnet's polarity to violently recycle buried garbage,
> dealing 59774 Plague damage to your target per charge.
> Lingering virulence deals 10% of the damage dealt to 5 nearby enemies over 6 sec. (20 Sec Cooldown)
"""
JUNKMAESTROS_MEGA_MAGNET.add_specs(*AGI_SPECS)


SCRAPFIELD_9001 = UndermineTrinket(
    spell_id=466673,
    cooldown=30,
    name="Scrapfield 9001",
    icon="inv_111_forcefieldmodule_steamwheedle.jpg",
    item=230026,
    event_type="buff",
)
"""Shield Proc when below 60% HP. (Tank only)

- Buff: 466673
- Debuff: 472170

> Equip: Falling below 60% health surrounds you with a protective vortex of junk,
> reducing damage taken by 50% for 15 sec or until 996802 damage is prevented.
> This effect may only occur every 30 sec.
> 
> After 20 sec without activating while in combat, the Scrapfield overloads
> to energize you with 2651 Haste for 12 sec.

"""
# SCRAPFIELD_9001.add_specs(*TANK.specs)


################################################################################
# Sprocketmonger Lockenstock


MISTER_LOCK_N_STALK = UndermineTrinket(
    spell_id=0,
    cooldown=20,
    name="Mister Lock-N-Stalk",
    icon="inv_111_healraydrone_gallywix.jpg",
    item=230193,
)
"""Random DMG Proc. Can swap between AoE or ST.

Precision Blasting
> Your spells and abilities have a high chance to lase your target for Precision Blasting,
> calling in Mister Lock-N-Stalk to deal 3555 Physical damage to your target.
> https://www.wowhead.com/ptr-2/spell=467492/precision-blasting

Mass Destruction
> Your spells and abilities have a high chance to lase enemies for Mass Destruction,
> calling in Mister Lock-N-Stalk to deal 2074 Fire damage split between your target and nearby enemies.
> https://www.wowhead.com/ptr-2/spell=467497/mass-destruction

"""
# MISTER_LOCK_N_STALK.add_specs(*DPS_SPECS)


MISTER_PICK_ME_UP = UndermineTrinket(
    spell_id=0,
    name="Mister Pick-Me-Up",
    icon="inv_111_healraydrone_bilgewater.jpg",
    item=230186,
)
"""random healing proc

> Your healing spells and abilities have a chance to summon Mister Pick-Me-Up for 6 sec,
> firing a healing beam every 2 sec that jumps between 5 injured allies to restore 72074 health each.
>
> Overhealing from this effect irradiates allies to deal Nature damage to nearby
> enemies over 1.5 sec, increased by additional overhealing.
"""

################################################################################
# One-Armed Bandit


GALLAGIO_BOTTLE_SERVICE = UndermineTrinket(
    spell_id=471214,
    duration=4,
    cooldown=90,
    name="Gallagio Bottle Service",
    icon="inv_111_underminegangsterdisguise.jpg",
    item=230188,
)
"""On-Use Healing (channel)

> Use: Become the pinnacle of Gallagio service excellence and dole out
> Kaja'Cola Mega-Lite to injured allies 10 times over 4 sec, healing them for
> 376075 and increasing their Speed by 1407 for 5 sec.
> The number of servings is increased by your Haste. (1 Min, 30 Sec Cooldown)

"""
GALLAGIO_BOTTLE_SERVICE.add_specs(*HEAL.specs)


HOUSE_OF_CARDS = UndermineTrinket(
    spell_id=466681,
    duration=15,
    cooldown=90,
    name="House of Cards",
    icon="inv_111_gallyjack_gallywix.jpg",
    item=23002,
)
"""On-Use mastery

Buffs:
- 466681 Mastery Buff
- 1219158 Stacked Deck

> Use: Deal yourself in, granting you 6604.2 to 8071.8 Mastery for 15 sec and
> stacking the deck. Stacking the deck increases the minimum Mastery on future
> hands by 244.6 until you leave combat, up to 3 times. (1 Min, 30 Sec Cooldown)
"""
HOUSE_OF_CARDS.add_specs(*ALL_SPECS)


################################################################################
# Mug'Zee


MUGS_MOXIE_JUG = UndermineTrinket(
    spell_id=0,
    name="Mug's Moxie Jug",
    icon="inv_111_blackbloodfueledcontainer.jpg",
    item=230192,
)
"""int main + crit proc

> Equip: Your spells have a chance to send you into a frenzy, granting you
> 742 Critical Strike for 15 sec. While frenzied, each spell cast grants an
> additional 742 Critical Strike but does not refresh the duration.
> This effect may only occur every 1 sec.
"""


ZEES_THUG_HOTLINE = UndermineTrinket(
    spell_id=0,
    name="Zee's Thug Hotline",
    icon="inv_111_remotecontrol_gallywix.jpg",
    item=230199,
)
"""agi/str main + dmg proc

> Equip: Your abilities have a chance to call a member of the Goon Squad to
> attack your target for 10 sec. Gaining Bloodlust or a similar effect summons the whole crew.
"""


################################################################################
# Gallywix


CHROMEBUSTIBLE_BOMB_SUIT = UndermineTrinket(
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


EYE_OF_KEZAN = UndermineTrinket(
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
