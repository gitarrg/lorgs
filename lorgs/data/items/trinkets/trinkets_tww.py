from lorgs.data.classes import *
from lorgs.models.wow_trinket import WowTrinket


################################################################################
# AraKara
# no on use trinkets


################################################################################
# Cinderbrew Meadery

CINDERBREW_STEIN = "Cinderbrew Stein"
"""Random Stat Proc

https://www.wowhead.com/item=219297/cinderbrew-stein

> Equip: Occasionally share a drink with allies who assist you in combat,
> granting them 700 of their primary stat for 15 sec and absorbing 19079 damage.
> You take a sip as well, granting 377 <Primary Stat> and absorbing 89032 damage.
>
> When you fall below 50% health, you take an emergency sip. This may only occur once every 1 min.
"""

RAVENOUS_HONEY_BUZZER = WowTrinket(
    spell_id=448904,
    cooldown=90,
    name="Ravenous Honey Buzzer",
    icon="inv_10_engineering_device_gadget1_color1.jpg",
    item=219298,
)
"""15yd Charge + split dmg

> Use: Call in a ravenous ally and ride off into the sunset (or $443387rad1 yds, whichever is closest),
> inflicting 161686 Fire damage split between all enemies you ride through. (1 Min, 30 Sec Cooldown)
"""
RAVENOUS_HONEY_BUZZER.add_specs(*STR_SPECS)
RAVENOUS_HONEY_BUZZER.add_specs(*AGI_SPECS)


SYNERGISTIC_BREWTERIALIZER = "Synergistic Brewterializer"
"""Random DMG Proc

https://www.wowhead.com/item=219299/synergistic-brewterializer

> Equip: Your spells have a chance to charge the device and request a Backfill Barrel
> near your target's location. Damaging the barrel causes it to explode,
> inflicting 84121 Fire damage split between nearby enemies.
"""


################################################################################
# City of Threads

# [Oppressive Orator's Larynx] = bad


################################################################################
# Darkflame Cleft
BURIN_OF_THE_CANDLE_KING = WowTrinket(
    spell_id=443529,
    cooldown=90,
    name="Burin of the Candle King",
    icon="inv_jewelcrafting_70_jeweledlockpick.jpg",
    item=219306,
)
"""On-Use Absorb

probably worth tracking some sort of buff, in case this gets played

> Use: Carve a wax copy of your target, which absorbs 50% of their damage taken.
> The absorption heats up the wax, causing it to melt after absorbing 264398 damage. (1 Min, 30 Sec Cooldown)

"""

CARVED_BLAZIKON_WAX = "[Carved Blazikon Wax]"
"""Vers Proc (15sec)

> Equip: Your spells have a chance to imbue the wax, causing it to form into a
> blazing candle for 15 sec which increases your Versatility by 1292, further
> increased by 136 while you remain within its light.
"""

CONDUCTORS_WAX_WHISTLE = "[Conductor's Wax Whistle]"
"""Random Damage Proc

> Equip: Your attacks have a chance to direct a Kobold Cart towards your target,
> sending a careening troop that collides with enemies, inflicting 50842 Physical
> damage split between enemies impacted.
"""

REMNANT_OF_DARKNESS = "[Remnant of Darkness]"
"""Accumulates stacks -> aoe damage split

> Equip: Your abilities have a chance to call the Darkness to you,
> increasing your <Primary Stat> by 245, up to 1225.  
> Upon reaching full power, the Darkness is unleashed, inflicting 99665 Shadow damage
> split between nearby enemies over 15 sec before fading back into the remnant.
"""

################################################################################
# Priory of the Sacred Flame
BURSTING_LIGHTSHARD = WowTrinket(
    spell_id=443536,
    cooldown=120,
    name="Bursting Lightshard",
    icon="inv_arathordungeon_fragment_color4.jpg",
    item=219310,
)
"""On-Use placed pet, pulses for Damage

> Use: Summon a Bursting Lightspawn which sacrifices its health to unleash Bursts of Light,
> inflicting 47520 Holy damage split between nearby enemies every 2 sec while it lives. (2 Min Cooldown)
"""

SIGNET_OF_THE_PRIORY = WowTrinket(
    spell_id=443531,
    cooldown=120,
    duration=20,
    name="Signet of the Priory",
    icon="inv_arathordungeon_signet_color1.jpg",
    item=219308,
    query=True,
)
"""On-Use secondary stat + party buff

> Use: Raise your signet to the Light, increasing your highest secondary stat by 2756 for 20 sec.
> Your act inspires nearby signetbearers within your party, granting them 73 of the same stat for 20 sec. (2 Min Cooldown)
"""
SIGNET_OF_THE_PRIORY.add_specs(*ALL_SPECS)


TOME_OF_LIGHTS_DEVOTION = "[Tome of Light's Devotion]"
"""Absorb and some one use. (Tank Only)

spell_id=443535
https://www.wowhead.com/item=219309/tome-of-lights-devotion

> Equip: Advance to the 50 Verses of Inner Resilience, reading as you are attacked.
> Inner Resilience increases your armor by 97 and grants your attacks a chance to
> invoke a ward which absorbs 3781 Magic damage. When finished, sift through the passages to another chapter.

> Valid only for tank specializations. (750ms cooldown)
> Use: Sift through the passages in the tome with increased Radiance. (1 Min, 30 Sec Cooldown)
"""


################################################################################
# The Dawnbreaker

# [Mereldar's Toll]


################################################################################
# The Rookery

CHARGED_STORMROOK_PLUME = WowTrinket(
    spell_id=443337,
    cooldown=90,
    name="Charged Stormrook Plume",
    icon="inv_achievement_dungeon_rookery.jpg",
    item=219294,
)
"""1sec cast -> charge to location + split damage

460469 = trigger
443337 = release

> Use: Hold out the feather for 11 sec to strike with the power of the storm,
> crashing down on the target location and inflicting 104053 Nature damage split
> between nearby enemies. (1 Min, 30 Sec Cooldown)
"""


ENTROPIC_SKARDYN_CORE = "[Entropic Skardyn Core]"
"""Random Int Proc

> Equip: Your spells have a chance to destabilize the void energy, releasing a corrupted fragment.
> Retrieving a fragment briefly infuses you with its power, increasing your Intellect by 1235 for 15 sec.

"""

SIGIL_OF_ALGARI_CONCORDANCE = "[Sigil of Algari Concordance]"
"""Random Pet Proc

> Equip: Your abilities have a chance to call an earthen ally to your aid, supporting you in combat. (15s cooldown)
"""

################################################################################
# Stonevault
# [High Speaker's Accretion]
# [Overclocked Gear-a-Rang Launcher]

WowTrinket(
    spell_id=443407,
    cooldown=90,
    duration=15,
    name="Skarmorak Shard",
    icon="inv_arathordungeon_fragment_color2.jpg",
    item=219300,
    ilvl=619,
).add_specs(*STR_SPECS)


################################################################################
# Operation: Floodgate
DARKFUSE_MEDICHOPPER = WowTrinket(
    spell_id=1220488,
    cooldown=120,
    duration=15,
    name="Darkfuse Medichopper",
    icon="inv_111_healraydrone_blackwater.jpg",
    item=232542,
)
"""On-Use Absorb + Vers on Target

> Use: Command the Medichopper to attach to your target, absorbing 134943 damage
> and granting them 1196 versatility for 15 sec.
> While attached, your healing spells have a chance to refuel the chopper,
> granting these bonuses to their host again. (2 Min Cooldown)

"""

GIGAZAPS_ZAP_CAP = "[Gigazap's Zap-Cap]"
"""Random Damage Proc

> Equip: Every 6 sec, Zap your target and 1 nearby enemy for 20752 Nature damage.
> Casting 30 spells Turbo-Charges you for 15 sec, doubling the frequency of your Zaps
> and upgrading them into Giga-Zaps, dealing 62256 Nature Damage instead. (750ms cooldown)
"""

IMPROVISED_SEAFORIUM_PACEMAKER = "[Improvised Seaforium Pacemaker]"
"""extendable Crit Buff every 60sec ?

> Equip: Repurpose a Seaforium charge to give your heart a kick, causing your first ability
> every 60 sec to trigger Explosive Adrenaline, granting 2916 Critical Strike for 15 sec.
>
> While exploding, Critical Strikes cause you to blow up again, extending this duration by 1 sec, up to 15 times.
"""

RINGING_RITUAL_MUD = WowTrinket(
    spell_id=1219102,
    cooldown=120,
    duration=10,
    name="Ringing Ritual Mud",
    icon="inv_misc_food_legion_goomolasses_pool.jpg",
    item=232543,
)
"""On-Use Absorb + pulse AoE

> Use: Become Mudborne, absorbing 7088217 damage and pulsing 291125 Nature damage split between nearby enemies over 10 sec.
>
> Periodic damage you take coalesces into pungent mud to feed the ritual, reducing this cooldown by 22 sec. (2 Min Cooldown)
"""
