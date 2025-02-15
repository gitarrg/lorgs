"""RaidZone and Bosses for Patch 10.0 T31: Vault of the Incarnates, first raid tier of Dragonflight."""

# IMPORT LOCAL LIBRARIES
from lorgs.models.raid_zone import RaidZone

from .eranog import ERANOG
from .terros import TERROS
from .primal_council import PRIMAL_COUNCIL
from .sennarth import SENNARTH
from .dathea import DATHEA
from .kurog import KUROG
from .broodkeeper_diurna import DIURNA
from .raszageth import RASZAGETH


################################################################################
#
#   Tier: 31 Vault of the Incarnates
#
################################################################################
VAULT_OF_THE_INCARNATES = RaidZone(
    id=31,
    name="Vault of the Incarnates",
    icon="achievement_raidprimalist_raid.jpg",
    bosses=[
        ERANOG,
        TERROS,
        PRIMAL_COUNCIL,
        SENNARTH,
        DATHEA,
        KUROG,
        DIURNA,
        RASZAGETH,
    ],
)
