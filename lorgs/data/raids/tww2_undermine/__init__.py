"""RaidZone and Bosses for Patch 11.1 Liberation of Undermine, second raid tier of The War Within.

Bosses:
    https://wago.tools/db2/DungeonEncounter?filter[MapID]=exact%3A2769&page=1

"""

# IMPORT LOCAL LIBRARIES
from lorgs.models.raid_zone import RaidZone
from lorgs.data.raids.tww2_undermine.cauldron import CAULDRON
from lorgs.data.raids.tww2_undermine.gallywix import GALLYWIX
from lorgs.data.raids.tww2_undermine.lockenstock import LOCKENSTOCK
from lorgs.data.raids.tww2_undermine.mugzee import MUGZEE
from lorgs.data.raids.tww2_undermine.one_armed_bandit import ONE_ARMED_BANDIT
from lorgs.data.raids.tww2_undermine.rik import RIK
from lorgs.data.raids.tww2_undermine.stix import STIX
from lorgs.data.raids.tww2_undermine.vexie import VEXIE
from lorgs.data.raids.tww2_undermine.trinkets import *


################################################################################
#
#   Tier: 42 Liberation of Undermine
#
################################################################################
LIBERATION_OF_UNDERMINE = RaidZone(
    id=42,
    name="Liberation of Undermine",
    icon="inv_achievement_zone_undermine.jpg",
    bosses=[
        VEXIE,
        CAULDRON,
        RIK,
        STIX,
        LOCKENSTOCK,
        ONE_ARMED_BANDIT,
        MUGZEE,
        GALLYWIX,
    ],
)
