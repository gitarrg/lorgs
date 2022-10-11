"""RaidZone and Bosses for Patch 10.0 T31: Vault of the Incarnates, first raid tier of Dragonflight."""
# pylint: disable=line-too-long
# pylint: disable=C0326  # spaces

# IMPORT LOCAL LIBRARIES
from .broodkeeper_diurna import DIURNA
from .dathea import DATHEA
from .eranog import ERANOG
from .kurog import KUROG
from .primal_council import PRIMAL_COUNCIL
from .raszageth import RASZAGETH
from .sennarth import SENNARTH
from .terros import TERROS
from lorgs.models.raid_zone import RaidZone


################################################################################################################################################################
#
#   Tier: 30 Vault of the Incarnates
#
################################################################################################################################################################
VAULT_OF_THE_INCARNATES = RaidZone(
    id=31,
    name="Vault of the Incarnates",
    bosses=[
        ERANOG,
        TERROS,
        PRIMAL_COUNCIL,
        SENNARTH,
        DATHEA,
        KUROG,
        DIURNA,
        RASZAGETH,
    ]
)
