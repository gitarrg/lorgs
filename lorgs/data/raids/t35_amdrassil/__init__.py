"""RaidZone and Bosses for Patch 10.2 T35: Amirdrassil, the Dream's Hope, third raid tier of Dragonflight."""

# IMPORT LOCAL LIBRARIES
from lorgs.data.raids.t35_amdrassil.council import COUNCIL_OF_DREAMS
from lorgs.data.raids.t35_amdrassil.fyrakk import FYRAKK
from lorgs.data.raids.t35_amdrassil.gnarlroot import GNARLROOT
from lorgs.data.raids.t35_amdrassil.igira import IGIRA
from lorgs.data.raids.t35_amdrassil.larodar import LARODAR
from lorgs.data.raids.t35_amdrassil.nymue import NYMUE
from lorgs.data.raids.t35_amdrassil.smolderon import SMOLDERON
from lorgs.data.raids.t35_amdrassil.tindral import TINDRAL
from lorgs.data.raids.t35_amdrassil.volcoross import VOLCOROSS
from lorgs.models.raid_zone import RaidZone


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
