"""Define the Evoker Class and all its Specs and Spells."""
# pylint: disable=line-too-long
# pylint: disable=bad-whitespace
# pylint: disable=wildcard-import
# pylint: disable=unused-wildcard-import
# fmt: off

# IMPORT LOCAL LIBRARIES
from lorgs.data.constants import *
from lorgs.data.roles import *
from lorgs.models.wow_class import WowClass
from lorgs.models.wow_spec import WowSpec
from lorgs.models.wow_spell import SpellTag


COLOR_BRONZE = "#e8bf46"
COLOR_BLACK = "#915f59"
COLOR_RED = "#eb3f3f"


################################################################################
# Class
#
EVOKER = WowClass(id=13, name="Evoker", color="#33937F")

################################################################################
# Specs
#
EVOKER_DEVASTATION = WowSpec(role=RDPS, wow_class=EVOKER, name="Devastation")
EVOKER_PRESERVATION = WowSpec(role=HEAL, wow_class=EVOKER, name="Preservation")
EVOKER_AUGMENTATION = WowSpec(role=RDPS, wow_class=EVOKER, name="Augmentation")


################################################################################
# Spells
#

# Defensives
EVOKER.add_spell(spell_id=363916, name="Obsidian Scales",    cooldown=150, duration=12, color=COLOR_BLACK,  icon="inv_artifact_dragonscales.jpg", show=False)
EVOKER.add_spell(spell_id=374348, name="Renewing Blaze",     cooldown=150, duration=8,  color=COLOR_RED,    icon="ability_evoker_masterylifebinder_red.jpg", show=False)
EVOKER.add_spell(spell_id=370553, name="Tip the Scales",     cooldown=120,              color=COLOR_BRONZE, icon="ability_evoker_tipthescales.jpg", show=False)
EVOKER.add_spell(spell_id=374227, name="Zephyr",             cooldown=120, duration=8,  color="#d6b969",    icon="ability_evoker_hoverblack.jpg", tags=[SpellTag.RAID_CD], show=False)
EVOKER.add_spell(spell_id=374968, name="Time Spiral",        cooldown=120, duration=10, color="#c4d669",    icon="ability_evoker_timespiral.jpg", tags=[SpellTag.RAID_CD], show=False)

# DPS
EVOKER_DEVASTATION.add_spell(spell_id=368847, name="Firestorm",  cooldown=20,  duration=12, color=COLOR_RED, icon="ability_evoker_firestorm.jpg")
EVOKER_DEVASTATION.add_spell(spell_id=375087, name="Dragonrage", cooldown=120, duration=14, color=COLOR_RED, icon="ability_evoker_dragonrage.jpg")


_filter_tip_the_scales = "IN RANGE FROM type = 'applybuff' AND ability.name = 'Tip the Scales' TO type = 'removebuff' AND ability.name = 'Tip the Scales' END"
tooltip_tip_the_scales_buffed = "Tip the Scales buffed."
EVOKER_DEVASTATION.add_spell(spell_id=382266, name="Fire Breath", cooldown=30, color=COLOR_RED, icon="ability_evoker_firebreath.jpg", extra_filter=_filter_tip_the_scales, tooltip=tooltip_tip_the_scales_buffed)
EVOKER_DEVASTATION.add_spell(spell_id=382411, name="Eternity Surge", cooldown=30, color="#308fbf", icon="ability_evoker_eternitysurge.jpg", extra_filter=_filter_tip_the_scales, tooltip=tooltip_tip_the_scales_buffed)


# HEAL
EVOKER_PRESERVATION.add_spell(spell_id=370960, name="Emerald Communion",  cooldown=180, duration=5,                      icon="ability_evoker_green_01.jpg", tags=[SpellTag.RAID_CD])
EVOKER_PRESERVATION.add_spell(spell_id=363534, name="Rewind",             cooldown=240,              color=COLOR_BRONZE, icon="ability_evoker_rewind.jpg", tags=[SpellTag.RAID_CD])
EVOKER_PRESERVATION.add_spell(spell_id=359816, name="Dreamflight",        cooldown=240, duration=15, color="#33a36d",    icon="ability_evoker_dreamflight.jpg", tags=[SpellTag.RAID_CD])
EVOKER_PRESERVATION.add_buff( spell_id=370562, name="Stasis",             cooldown=90,               color=COLOR_BRONZE, icon="ability_evoker_stasis.jpg", tags=[SpellTag.RAID_CD])


# Augmentation
EVOKER_AUGMENTATION.add_buff( spell_id=395296, name="Ebon Might Buff",                            color="#bf8330", icon="spell_sarkareth.jpg", show=False)
EVOKER_AUGMENTATION.add_spell(spell_id=403631, name="Breath of Eons",  cooldown=120, duration=12, color="#e4e267", icon="ability_evoker_breathofeons.jpg")
EVOKER_AUGMENTATION.add_spell(spell_id=404977, name="Time Skip",       cooldown=180,              color="#e8bf46", icon="ability_evoker_timeskip.jpg")
