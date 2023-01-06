"""Buffs/Spells from other Specs. eg.: Power Infusion or PainSup."""

# IMPORT LOCAL LIBRARIES
from lorgs.data.classes import *  # for Colors
from lorgs.data.classes import ALL_SPECS
from lorgs.data.classes.other import OTHER_BUFFS
from lorgs.data.constants import *


BLOODLUST = OTHER_BUFFS.add_buff(color="#5465ff", spell_id=2825, duration=40, name="Bloodlust", icon="spell_nature_bloodlust.jpg")
BLOODLUST.add_variation(32182)  # Heroism
BLOODLUST.add_variation(80353)  # Time Warp
BLOODLUST.add_variation(264667) # Primal Rage
BLOODLUST.add_variation(272678) # Primal Rage
BLOODLUST.add_variation(272678) # Primal Rage
BLOODLUST.add_variation(390386) # Fury of the Aspects

################################################################################
# External Defensive
#
OTHER_BUFFS.add_buff(color=DRUID.color,   spell_id=102342, cooldown=90,  duration=12, name="Ironbark",                icon="spell_druid_ironbark.jpg")
OTHER_BUFFS.add_buff(color=PRIEST.color,  spell_id=33206,  cooldown=180, duration=8,  name="Pain Suppression",        icon="spell_holy_painsupression.jpg")
OTHER_BUFFS.add_buff(color=PRIEST.color,  spell_id=47788,  cooldown=180,              name="Guardian Spirit",         icon="spell_holy_guardianspirit.jpg")
OTHER_BUFFS.add_buff(color=PALADIN.color, spell_id=1022,   cooldown=300, duration=10, name="Blessing of Protection",  icon="spell_holy_sealofprotection.jpg")
OTHER_BUFFS.add_buff(color=PALADIN.color, spell_id=6940,   cooldown=120,              name="Blessing of Sacrifice",   icon="spell_holy_sealofsacrifice.jpg")
OTHER_BUFFS.add_buff(color=MONK.color,    spell_id=116849, cooldown=120,              name="Life Cocoon",             icon="ability_monk_chicocoon.jpg")
OTHER_BUFFS.add_buff(color=WARRIOR.color, spell_id=335198, cooldown=30,               name="Safeguard",               icon="ability_warrior_safeguard.jpg")  # Warrior Intervene Conduit

################################################################################
# External Power Gains
#
POWER_INFUSION    = OTHER_BUFFS.add_buff(color="#f7c625", spell_id=10060,  cooldown=120, duration=20, name="Power Infusion",      icon="spell_holy_powerinfusion.jpg")
INNERVATE         = OTHER_BUFFS.add_buff(color="#3b97ed", spell_id=29166,  cooldown=180, duration=10, name="Innervate",           icon="spell_nature_lightning.jpg")
BLESSING_OF_AUTUMN = OTHER_BUFFS.add_buff(color=PALADIN.color, spell_id=388010, cooldown=45, duration=30, name="Blessing of Autumn", icon="ability_ardenweald_paladin_autumn.jpg")

################################################################################

for spell in (OTHER_BUFFS.spells + OTHER_BUFFS.buffs):
    spell.show = False


for s in ALL_SPECS:
    s.add_spells(*OTHER_BUFFS.spells)
    s.add_buffs(*OTHER_BUFFS.buffs)
