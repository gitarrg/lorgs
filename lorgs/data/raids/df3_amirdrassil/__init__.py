"""RaidZone and Bosses for Patch 10.2 T35: Amirdrassil, the Dream's Hope, third raid tier of Dragonflight."""

# IMPORT LOCAL LIBRARIES
from lorgs.models.raid_zone import RaidZone
from lorgs.data.raids.df3_amirdrassil.council import COUNCIL_OF_DREAMS
from lorgs.data.raids.df3_amirdrassil.fyrakk import FYRAKK
from lorgs.data.raids.df3_amirdrassil.gnarlroot import GNARLROOT
from lorgs.data.raids.df3_amirdrassil.igira import IGIRA
from lorgs.data.raids.df3_amirdrassil.larodar import LARODAR
from lorgs.data.raids.df3_amirdrassil.nymue import NYMUE
from lorgs.data.raids.df3_amirdrassil.smolderon import SMOLDERON
from lorgs.data.raids.df3_amirdrassil.tindral import TINDRAL
from lorgs.data.raids.df3_amirdrassil.volcoross import VOLCOROSS
from lorgs.data.raids.df3_amirdrassil.trinkets import *


################################################################################
#
#   Tier: 35 Amirdrassil, the Dream's Hope
#
################################################################################
AMIRDRASSIL = RaidZone(
    id=35,
    name="Amirdrassil, the Dream's Hope",
    bosses=[
        GNARLROOT,
        IGIRA,
        VOLCOROSS,
        COUNCIL_OF_DREAMS,
        LARODAR,
        NYMUE,
        SMOLDERON,
        TINDRAL,
        FYRAKK,
    ],
)
