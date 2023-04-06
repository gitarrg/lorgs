"""RaidZone and Bosses for Patch 10.1 T33: Aberrus, the Shadowed Crucible, second raid tier of Dragonflight."""

# IMPORT LOCAL LIBRARIES
from lorgs.models.raid_zone import RaidZone
from lorgs.data.raids.t33_aberrus.kazzara import KAZZARA
from lorgs.data.raids.t33_aberrus.molgoth import MOLGOTH
from lorgs.data.raids.t33_aberrus.forgotten_experiments import FORGOTTEN_EXPERIMENTS
from lorgs.data.raids.t33_aberrus.assault_of_the_zaqali import ASSAULT_OF_THE_ZAQALI
from lorgs.data.raids.t33_aberrus.rashok import RASHOK
from lorgs.data.raids.t33_aberrus.zskarn import ZSKARN
from lorgs.data.raids.t33_aberrus.magmorax import MAGMORAX
from lorgs.data.raids.t33_aberrus.neltharion import NELTHARION
from lorgs.data.raids.t33_aberrus.sarkareth import SARKARETH


################################################################################
#
#   Tier: 33 Aberrus, the Shadowed Crucible
#
################################################################################
ABERRUS = RaidZone(
    id=33,
    name="Aberrus, the Shadowed Crucible",
    bosses=[
        KAZZARA,
        MOLGOTH,
        FORGOTTEN_EXPERIMENTS,
        ASSAULT_OF_THE_ZAQALI,
        RASHOK,
        ZSKARN,
        MAGMORAX,
        NELTHARION,
        SARKARETH,
    ],
)
