"""War Within Season 2."""

from lorgs.data.expansions.battle_for_azeroth.dungeons.mechagon_workshop import MECHAGON_WORKSHOP
from lorgs.data.expansions.battle_for_azeroth.dungeons.motherlode import THE_MOTHERLODE
from lorgs.data.expansions.shadowlands.dungeons.theater_of_pain import THEATER_OF_PAIN
from lorgs.data.expansions.the_war_within.dungeons.cinderbrew_meadery import CINDERBREW_MEADERY
from lorgs.data.expansions.the_war_within.dungeons.darkflame_cleft import DARKFLAME_CLEFT
from lorgs.data.expansions.the_war_within.dungeons.operation_floodgate import OPERATION_FLOODGATE
from lorgs.data.expansions.the_war_within.dungeons.priory_of_the_sacred_flame import PRIORY_OF_THE_SACRED_FLAME
from lorgs.data.expansions.the_war_within.dungeons.the_rookery import THE_ROOKERY
from lorgs.data.expansions.the_war_within.raids.undermine import LIBERATION_OF_UNDERMINE
from lorgs.models.season import Season


TWW_SEASON2 = Season(
    name="TWW Season 2",
    slug="tww_2",
    ilvl=678,
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
