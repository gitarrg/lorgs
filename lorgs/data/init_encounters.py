#!/usr/bin/env python
"""Models for Raids and RaidBosses."""

# pylint: disable=line-too-long
# pylint: disable=C0326  # spaces

# IMPORT LOCAL LIBRARIES
from lorgs.models.encounters import RaidZone

################################################################################################################################################################
#
#   Tier: 26 Castle Nathria
#
################################################################################################################################################################
CASTLE_NATHRIA = RaidZone(id=26, name="Castle Nathria")

################################################################################
# 01: Shriekwing
SHRIEKWING = CASTLE_NATHRIA.add_boss(id=2398, name="Shriekwing")
SHRIEKWING.add_event(event_type="cast",      spell_id=345397, duration=12, color="#c94444", name="Wave of Blood",   icon="ability_ironmaidens_whirlofblood.jpg")
SHRIEKWING.add_event(event_type="cast",      spell_id=342863,              color="#c94444", name="Echoing Screech", icon="spell_nature_wispsplode.jpg")
SHRIEKWING.add_event(event_type="applybuff", spell_id=328921, duration=33, color="#999999", name="Blood Shroud",    icon="ability_deathwing_bloodcorruption_earth.jpg")

CASTLE_NATHRIA.add_boss(id=2418, name="Huntsman Altimor")

################################################################################
# 03: Hungering Destroyer
HUNGERING_DESTROYER = CASTLE_NATHRIA.add_boss(id=2383, name="Hungering Destroyer")
HUNGERING_DESTROYER.add_event(event_type="begincast", spell_id=334522, duration=10, color="#17e3be", name="Consume",  icon="ability_argus_deathfog.jpg")
HUNGERING_DESTROYER.add_event(event_type="cast",      spell_id=329455, duration=10, color="#d65656", name="Desolate", icon="ability_argus_soulburst.jpg")

CASTLE_NATHRIA.add_boss(id=2402, name="Sun King's Salvation")



CASTLE_NATHRIA.add_boss(id=2405, name="Artificer Xy'mox")

CASTLE_NATHRIA.add_boss(id=2406, name="Lady Inerva Darkvein")

COUNCIL_OF_BLOOD = CASTLE_NATHRIA.add_boss(id=2412, name="The Council of Blood")
COUNCIL_OF_BLOOD.add_event(spell_id=330959, duration=36, color="#1a86dc", name="Danse Macabre", icon="ability_rogue_shadowdance.jpg")
COUNCIL_OF_BLOOD.add_event(spell_id=331634, duration=6, color="#6735d4", name="Dark Recital", icon="ability_warlock_soullink.jpg")
COUNCIL_OF_BLOOD.add_event(event_type="applydebuff", spell_id=347350, duration=30, color="#d65656", name="Dancing Fever", icon="ability_deathknight_hemorrhagicfever.jpg")


################################################################################
# 08: Sludgefist
SLUDGEFIST = CASTLE_NATHRIA.add_boss(id=2399, name="Sludgefist")
SLUDGEFIST.add_event(event_type="cast",      spell_id=332687, name="Colossal Roar",      icon="ability_garrosh_hellscreams_warsong.jpg", duration=2, color="#c94444")
SLUDGEFIST.add_event(event_type="cast",      spell_id=332318, name="Destructive Stomp",  icon="spell_nature_earthquake.jpg", duration=4, color="#d69429")
SLUDGEFIST.add_event(event_type="applybuff", spell_id=331314, name="Destructive Impact", icon="spell_frost_stun.jpg", duration=12, color="#34c0eb")

################################################################################
# 09: Stone Legion Generals
SLG = CASTLE_NATHRIA.add_boss(id=2417, name="Stone Legion Generals")
SLG.add_event(event_type="cast",      spell_id=342544, name="Pulverizing Meteor",  icon="inv_elementalearth2.jpg", duration=2, color="#d69429")
SLG.add_event(event_type="cast",      spell_id=334498, name="Seismic Upheaval",  icon="spell_nature_earthquake.jpg", duration=5, color="#d69429")
SLG.add_event(event_type="cast",      spell_id=334765, name="Heart Rend",  icon="spell_fire_flameblades.jpg", duration=36, color="#d69429", show=False)

################################################################################
# 10: Sire Denathrius
SIRE_DENATHRIUS = CASTLE_NATHRIA.add_boss(id=2407, name="Sire Denathrius")
SIRE_DENATHRIUS.add_event(event_type="cast", spell_id=326994, duration=3.5, color="#c94444", name="Blood Price",           icon="ability_ironmaidens_whirlofblood.jpg")
SIRE_DENATHRIUS.add_event(event_type="cast", spell_id=326707, duration=3,   color="#0083ff", name="Cleansing Pain",        icon="spell_animarevendreth_wave.jpg")
SIRE_DENATHRIUS.add_event(event_type="cast", spell_id=327122, duration=6,   color="#ffcf00", name="Ravage",                icon="spell_shadow_corpseexplode.jpg", show=False)

SIRE_DENATHRIUS.add_event(event_type="cast", spell_id=328117, duration=10,  color="#ffffff", name="March of the Penitent", icon="sha_spell_shadow_shadesofdarkness_nightmare.jpg")

# P2
SIRE_DENATHRIUS.add_event(event_type="cast", spell_id=333932, duration=0, color="#c94444", name="Hand of Destruction",     icon="spell_shadow_unholystrength.jpg")
SIRE_DENATHRIUS.add_event(event_type="cast", spell_id=329943, duration=0, color="#c94444", name="Impale",                  icon="ability_backstab.jpg")

# P3
SIRE_DENATHRIUS.add_event(event_type="cast", spell_id=332937, duration=6,   color="#ffcf00", name="Ravage",                icon="spell_shadow_corpseexplode.jpg", show=False)
SIRE_DENATHRIUS.add_event(event_type="cast", spell_id=332619, duration=3,   color="#0083ff", name="Shattering Pain",       icon="sha_spell_fire_blueflamestrike_nightmare.jpg")

CASTLE_NATHRIA_BOSSES = CASTLE_NATHRIA.bosses


################################################################################################################################################################
#
#   Tier: 27 Sanctum of Domination
#
################################################################################################################################################################
SANCTUM_OF_DOMINATION = RaidZone(id=28, name="Sanctum of Domination")

TARRAGRUE = SANCTUM_OF_DOMINATION.add_boss(id=2423, name="The Tarragrue")

EYE_OF_THE_JAILER = SANCTUM_OF_DOMINATION.add_boss(id=2433, name="The Eye of the Jailer")
EYE_OF_THE_JAILER.add_event(event_type="cast", spell_id=349030, duration=8, color="#24c9b1", name="Titanic Death Gaze",  icon="ability_argus_deathfog.jpg")
EYE_OF_THE_JAILER.add_event(event_type="cast", spell_id=350828, duration=2, color="#ede080", name="Deathlink",           icon="ability_felarakkoa_eyeofterrok.jpg")
EYE_OF_THE_JAILER.add_event(event_type="applydebuff", spell_id=355240, duration=9, color="#db8823", name="Scorn & Ire",           icon="ability_xavius_darkruination.jpg")


THE_NINE = SANCTUM_OF_DOMINATION.add_boss(id=2429, name="The Nine")
THE_NINE.add_event(event_type="cast", spell_id=355294, duration=12, color="#a1b2cc", name="Resentment", icon="spell_animamaw_buff.jpg")


REMNANT = SANCTUM_OF_DOMINATION.add_boss(id=2432, name="Remnant of Ner'zhul")
REMNANT.add_event(event_type="cast", spell_id=350469, duration=10, color="#9e4cc2", name="Malevolence", icon="ability_warlock_eradication.jpg")
REMNANT.add_event(event_type="cast", spell_id=351066, duration=0, color="#24cbd1", name="Shatter", icon="achievement_boss_lichking.jpg")
REMNANT.add_event(event_type="cast", spell_id=351073, duration=0, color="#24cbd1", name="Malevolence", icon="inv_misc_desecrated_platechest.jpg")
REMNANT.add_event(event_type="cast", spell_id=351067, duration=0, color="#24cbd1", name="Malevolence", icon="inv_misc_desecrated_plategloves.jpg")


SOULRENDER = SANCTUM_OF_DOMINATION.add_boss(id=2434, name="Soulrender Dormazain")
SOULRENDER.add_event(event_type="removedebuff", spell_id=348987, duration=9, color="#b07f6b", name="Break Shackles",           icon="inv_belt_18.jpg")
SOULRENDER.add_event(event_type="cast", spell_id=350615, duration=0, color="#24cbd1", name="Adds", icon="inv_mawguardpet_red.jpg")
SOULRENDER.add_event(event_type="cast", spell_id=352933, duration=30, color="#4cb840", name="Dance", icon="spell_animarevendreth_wave.jpg")


PAINSMITH = SANCTUM_OF_DOMINATION.add_boss(id=2430, name="Painsmith Raznal")
PAINSMITH.add_event(event_type="cast", spell_id=359033, duration=45, color="#30c235", name="Intermission",  icon="ability_mage_moltenarmor.jpg")
PAINSMITH.add_event(event_type="cast", spell_id=355571, duration=6, color="#3fd4cf", name="Axe",           icon="inv_axe_2h_mawraid_diff.jpg")
PAINSMITH.add_event(event_type="cast", spell_id=348513, duration=6, color="#3fd4cf", name="Hammer",        icon="inv_mace_2h_maw_c_01.jpg")
PAINSMITH.add_event(event_type="cast", spell_id=355787, duration=6, color="#3fd4cf", name="Scythe",        icon="inv_polearm_2h_mawnecromancerboss_d_01_grey.jpg")
# we only filter tank debuffs to minimize the number of events returned
PAINSMITH.add_event(event_type="applydebuff", spell_id=356870, duration=1.5, color="#db5f39", name="Flameclasp Trap",  icon="ability_hunter_steeltrap.jpg", extra_filter="target.role='tank'")


GUARDIAN = SANCTUM_OF_DOMINATION.add_boss(id=2436, name="Guardian of the First Ones")
GUARDIAN.add_event(event_type="cast", spell_id=352538, duration=5, color="#24d1ce", name="Purging Protocol",  icon="spell_progenitor_areadenial.jpg")
GUARDIAN.add_event(event_type="cast", spell_id=350732, duration=2, color="#a42cd4", name="Sunder",            icon="inv_warbreaker.jpg")
GUARDIAN.add_event(event_type="cast", spell_id=355352, duration=2, color="#d4a72c", name="Obliterate",        icon="spell_progenitor_orb2.jpg")
GUARDIAN.add_event(event_type="cast", spell_id=352589, duration=6, color="#75d42c", name="Meltdown",          icon="spell_progenitor_nova.jpg")


FATESCRIBE = SANCTUM_OF_DOMINATION.add_boss(id=2431, name="Fatescribe Roh-Kalo")
FATESCRIBE.add_event(event_type="cast", spell_id=354265, duration=6, color="#af24ff", name="Twist Fate",  icon="spell_animamaw_debuff.jpg")
FATESCRIBE.add_event(event_type="cast", spell_id=351680, duration=8, color="#ffda24", name="Destiny",  icon="spell_animamaw_buff.jpg")
FATESCRIBE.add_event(event_type="applybuff", spell_id=357739, duration=0, color="#4bbf68", name="Intermisson Start",  icon="spell_shadow_painfulafflictions.jpg", until={"event_type": "removebuff", "spell_id": 357739})


KELTHUZAD = SANCTUM_OF_DOMINATION.add_boss(id=2422, name="Kel'Thuzad")
KELTHUZAD.add_event(event_type="applydebuff", spell_id=346530, duration=10, color="#ff4538", name="Spike",  icon="ability_mage_coldasice.jpg", extra_filter="target.role='tank'")
KELTHUZAD.add_event(event_type="cast", spell_id=348756, duration=8, color="#03eaff", name="Frost Blast",  icon="spell_frost_glacier.jpg")
KELTHUZAD.add_event(event_type="begincast", spell_id=352293, color="#30c235", name="Intermisson",  icon="spell_shadow_painfulafflictions.jpg", until={"event_type": "begincast", "spell_id": 352355})
KELTHUZAD.add_event(event_type="cast", spell_id=348071, duration=0, color="#03fcc6", name="Soul Fracture",  icon="spell_necro_deathlyecho.jpg", show=False)
KELTHUZAD.add_event(event_type="cast", spell_id=354198, duration=20, color="#c7eaff", name="Howling Blizzard",  icon="spell_frost_arcticwinds.jpg", show=False)


SYLVANAS = SANCTUM_OF_DOMINATION.add_boss(id=2435, name="Sylvanas Windrunner")
SYLVANAS.add_event(event_type="cast", spell_id=347741, duration=9, color="#228c89", name="Veil of Darkness",        icon="ability_argus_deathfog.jpg")
SYLVANAS.add_event(event_type="cast", spell_id=351353, duration=9, color="#b1c4c3", name="Orbs",        icon="spell_animamaw_orb.jpg")

DEFAULT_BOSS = TARRAGRUE

SANCTUM_OF_DOMINATION_BOSSES = SANCTUM_OF_DOMINATION.bosses
