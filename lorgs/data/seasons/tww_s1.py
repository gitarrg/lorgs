"""War Within Season 2."""

from lorgs.data.dungeons.bfa.siege_of_boralus import SIEGE_OF_BORALUS
from lorgs.data.dungeons.cata.grim_batol import GRIM_BATOL
from lorgs.data.dungeons.sl.mists import MISTS_OF_TIRNA_SCITHE
from lorgs.data.dungeons.sl.necrotic_wake import NECROTIC_WAKE
from lorgs.data.dungeons.tww.ara_kara import ARA_KARA
from lorgs.data.dungeons.tww.city_of_threads import CITY_OF_THREADS
from lorgs.data.dungeons.tww.dawnbreaker import DAWNBREAKER
from lorgs.data.dungeons.tww.stonevault import STONEVAULT
from lorgs.data.raids.tww1_nerubar_palace import NERUBAR_PALACE
from lorgs.models.season import Season


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
