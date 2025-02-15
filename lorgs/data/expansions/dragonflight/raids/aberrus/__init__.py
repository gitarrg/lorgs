"""RaidZone and Bosses for Patch 10.1 T33: Aberrus, the Shadowed Crucible, second raid tier of Dragonflight."""

# IMPORT LOCAL LIBRARIES
from lorgs.models.raid_zone import RaidZone
from .kazzara import KAZZARA
from .amalgamation_chamber import AMALGAMATION_CHAMBER
from .forgotten_experiments import FORGOTTEN_EXPERIMENTS
from .assault_of_the_zaqali import ASSAULT_OF_THE_ZAQALI
from .rashok import RASHOK
from .zskarn import ZSKARN
from .magmorax import MAGMORAX
from .neltharion import NELTHARION
from .sarkareth import SARKARETH
from .trinkets import *


################################################################################
#
#   Tier: 33 Aberrus, the Shadowed Crucible
#
################################################################################
ABERRUS = RaidZone(
    id=33,
    name="Aberrus, the Shadowed Crucible",
    icon="inv_achievement_raiddragon_raid.jpg",
    bosses=[
        KAZZARA,
        AMALGAMATION_CHAMBER,
        FORGOTTEN_EXPERIMENTS,
        ASSAULT_OF_THE_ZAQALI,
        RASHOK,
        ZSKARN,
        MAGMORAX,
        NELTHARION,
        SARKARETH,
    ],
)
