"""RaidZone and Bosses for Patch 10.2 T35: Amirdrassil, the Dream's Hope, third raid tier of Dragonflight."""

# IMPORT LOCAL LIBRARIES
from lorgs.models.raid_zone import RaidZone
from .council import COUNCIL_OF_DREAMS
from .fyrakk import FYRAKK
from .gnarlroot import GNARLROOT
from .igira import IGIRA
from .larodar import LARODAR
from .nymue import NYMUE
from .smolderon import SMOLDERON
from .tindral import TINDRAL
from .volcoross import VOLCOROSS
from .trinkets import *


################################################################################
#
#   Tier: 35 Amirdrassil, the Dream's Hope
#
################################################################################
AMIRDRASSIL = RaidZone(
    id=35,
    name="Amirdrassil, the Dream's Hope",
    icon="inv_achievement_raidemeralddream_raid.jpg",
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
