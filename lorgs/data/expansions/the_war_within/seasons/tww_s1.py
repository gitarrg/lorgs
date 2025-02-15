"""War Within Season 2."""

# IMPORT LOCAL LIBRARIES
from lorgs.models.season import Season

# Dungeons
from lorgs.data.expansions.battle_for_azeroth import SIEGE_OF_BORALUS
from lorgs.data.expansions.cataclysm import GRIM_BATOL
from lorgs.data.expansions.shadowlands import MISTS_OF_TIRNA_SCITHE
from lorgs.data.expansions.shadowlands import NECROTIC_WAKE
from lorgs.data.expansions.the_war_within import ARA_KARA
from lorgs.data.expansions.the_war_within import CITY_OF_THREADS
from lorgs.data.expansions.the_war_within import DAWNBREAKER
from lorgs.data.expansions.the_war_within import STONEVAULT

# Raids
from lorgs.data.expansions.the_war_within import NERUBAR_PALACE


TWW_SEASON1 = Season(
    name="TWW Season 1",
    slug="tww_s1",
    ilvl=639,
    raids=[
        NERUBAR_PALACE,
    ],
    dungeons=[
        ARA_KARA,
        CITY_OF_THREADS,
        DAWNBREAKER,
        STONEVAULT,
        MISTS_OF_TIRNA_SCITHE,
        NECROTIC_WAKE,
        SIEGE_OF_BORALUS,
        GRIM_BATOL,
    ],
)
