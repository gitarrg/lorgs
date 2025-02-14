"""War Within Season 2."""

from lorgs.data.dungeons.bfa.mechagon_workshop import MECHAGON_WORKSHOP
from lorgs.data.dungeons.bfa.motherlode import THE_MOTHERLODE
from lorgs.data.dungeons.sl.theater_of_pain import THEATER_OF_PAIN
from lorgs.data.dungeons.tww.cinderbrew_meadery import CINDERBREW_MEADERY
from lorgs.data.dungeons.tww.darkflame_cleft import DARKFLAME_CLEFT
from lorgs.data.dungeons.tww.operation_floodgate import OPERATION_FLOODGATE
from lorgs.data.dungeons.tww.priory_of_the_sacred_flame import PRIORY_OF_THE_SACRED_FLAME
from lorgs.data.dungeons.tww.the_rookery import THE_ROOKERY
from lorgs.data.raids.tww2_undermine import LIBERATION_OF_UNDERMINE
from lorgs.models.season import Season


TWW_SEASON2 = Season(
    name="tww_s2",
    ilvl=678,  # 6/6 Myth Track
    domain="ptr2",
    raids=[
        LIBERATION_OF_UNDERMINE,
    ],
    dungeons=[
        CINDERBREW_MEADERY,
        DARKFLAME_CLEFT,
        PRIORY_OF_THE_SACRED_FLAME,
        THE_ROOKERY,
        OPERATION_FLOODGATE,
        THEATER_OF_PAIN,
        MECHAGON_WORKSHOP,
        THE_MOTHERLODE,
    ],
)
