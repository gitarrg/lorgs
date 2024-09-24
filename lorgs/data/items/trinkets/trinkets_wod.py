from lorgs.data.classes import *
from lorgs.models.wow_trinket import WowTrinket


################################################################################
# Everbloom
#

WowTrinket(
    spell_id=429257,
    color="#39d31a",
    cooldown=90,
    name="Witherbark's Branch",
    icon="inv_misc_branch_01.jpg",
    item=109999,
    ilvl=483,
    query=False,
).add_specs(*AGI_SPECS)
