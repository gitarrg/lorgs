"""Buffs/Spells from other Specs. eg.: Power Infusion or PainSup."""


from lorgs.data.classes import ALL_SPECS
from lorgs.data.classes import *  # for Colors
from lorgs.data.classes.other import OTHER_BUFFS
from lorgs.data.constants import *
from lorgs.models.wow_class import WowClass


# EXTERNALS = WowClass(id=1004, name="External Buffs")  # dummy container


BLOODLUST = OTHER_BUFFS.add_buff(color="#5465ff", spell_id=2825, duration=40, name="Bloodlust", icon="spell_nature_bloodlust.jpg")
BLOODLUST.add_variation(32182)  # Heroism
BLOODLUST.add_variation(80353)  # Time Warp
BLOODLUST.add_variation(264667) # Primal Rage
BLOODLUST.add_variation(272678) # Primal Rage

################################################################################
# External Defensive
#
IRONBARK = OTHER_BUFFS.add_buff(color=DRUID.color,   spell_id=102342, cooldown=90,  duration=12, name="Ironbark",                icon="spell_druid_ironbark.jpg")
PAINSUP  = OTHER_BUFFS.add_buff(color=PRIEST.color,  spell_id=33206,  cooldown=180, duration=8,  name="Pain Suppression",        icon="spell_holy_painsupression.jpg")
GUARDIAN = OTHER_BUFFS.add_buff(color=PRIEST.color,  spell_id=47788,  cooldown=180,              name="Guardian Spirit",         icon="spell_holy_guardianspirit.jpg")
SAC      = OTHER_BUFFS.add_buff(color=PALADIN.color, spell_id=1022,   cooldown=300, duration=10, name="Blessing of Protection",  icon="spell_holy_sealofprotection.jpg")
COCOON   = OTHER_BUFFS.add_buff(color=MONK.color,    spell_id=116849, cooldown=120,              name="Life Cocoon",             icon="ability_monk_chicocoon.jpg")


################################################################################
# External Power Gains
#
POWER_INFUSION    = OTHER_BUFFS.add_buff(color="#f7c625", spell_id=10060,  cooldown=120, duration=20, name="Power Infusion",      icon="spell_holy_powerinfusion.jpg")
KYRIAN_BOND       = OTHER_BUFFS.add_buff(color=COL_KYR,   spell_id=327022,               duration=0,  name="Kindred Empowerment", icon="spell_animabastion_beam.jpg")
BENEVOLENT_FAERIE = OTHER_BUFFS.add_buff(color=COL_NF,    spell_id=327710,               duration=20, name="Benevolent Faerie",   icon="spell_animaardenweald_orb.jpg")
INNERVATE         = OTHER_BUFFS.add_buff(color="#3b97ed", spell_id=29166,  cooldown=180, duration=10, name="Innervate",           icon="spell_nature_lightning.jpg")


################################################################################
# Other
#
FLESHCRAFT        = OTHER_BUFFS.add_buff(color=COL_NECRO,  spell_id=324867, cooldown=120, duration=15, name="Fleshcraft",          icon="ability_necrolord_fleshcraft.jpg")


################################################################################

for spell in (OTHER_BUFFS.spells + OTHER_BUFFS.buffs):
    spell.show = False


for s in ALL_SPECS:
    s.add_spells(*OTHER_BUFFS.spells)
    s.add_buffs(*OTHER_BUFFS.buffs)
