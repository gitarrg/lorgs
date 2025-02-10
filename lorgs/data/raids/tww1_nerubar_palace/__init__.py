"""RaidZone and Bosses for Patch 11.0 Nerub-ar Palace, first raid tier of The War Within."""

# IMPORT LOCAL LIBRARIES
from lorgs.models.raid_zone import RaidZone
from lorgs.data.raids.tww1_nerubar_palace.ulgrax import ULGRAX
from lorgs.data.raids.tww1_nerubar_palace.bloodbound_horror import BLOODBOUND_HORROR
from lorgs.data.raids.tww1_nerubar_palace.sikran import SIKRAN
from lorgs.data.raids.tww1_nerubar_palace.rashanan import RASHANAN
from lorgs.data.raids.tww1_nerubar_palace.ovinax import OVINAX
from lorgs.data.raids.tww1_nerubar_palace.kyveza import KYVEZA
from lorgs.data.raids.tww1_nerubar_palace.silken_court import SILKEN_COURT
from lorgs.data.raids.tww1_nerubar_palace.ansurek import ANSUREK
from lorgs.data.raids.tww1_nerubar_palace.trinkets import *


################################################################################
#
#   Tier: 38 Nerub-ar Palace
#
################################################################################
NERUBAR_PALACE = RaidZone(
    id=38,
    name="Nerub-ar Palace",
    icon="achievement_zone_azjkahet.jpg",
    bosses=[
        ULGRAX,
        BLOODBOUND_HORROR,
        SIKRAN,
        RASHANAN,
        OVINAX,
        KYVEZA,
        SILKEN_COURT,
        ANSUREK,
    ],
)
