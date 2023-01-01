"""API Routes to get and update Comp Rankings."""
from __future__ import annotations

# IMPORT STANDARD LIBRARIES
import typing

# IMPORT THIRD PARTY LIBRARIES
import fastapi

# IMPORT LOCAL LIBRARIES
from lorgs.models import warcraftlogs_comp_ranking
from lorgs.models.raid_boss import RaidBoss
from lorrgs_api.routes import api_tasks


router = fastapi.APIRouter()


@router.get("/comp_ranking/{boss_slug}")
async def get_comp_ranking(response: fastapi.Response, boss_slug: str):
    """Fetch comp rankings for a given boss encounter.

    Args:
        boss_slug (str): name of the boss (full_name_slug)
    """
    # shorter cache timeout for the start of the tier (where frequent changes happen)
    response.headers["Cache-Control"] = "max-age=300"
    try:
        # NOTE: we return the raw json,
        # no need to parse the data
        return warcraftlogs_comp_ranking.CompRanking.get_json(boss_slug=boss_slug)
    except KeyError:
        raise fastapi.HTTPException(status_code=404, detail="Invalid Boss")


################################################################################
# Tasks
#
@router.get("/task/load_comp_ranking/{boss_slug}")
async def task_load_comp_rankings(boss_slug: str = "all", limit: int = 50, clear: bool = False):
    """Submit a scheduled task to update a single or all Comp Rankings."""
    kwargs = {"limit": limit, "clear": clear}

    # expand bosses
    if boss_slug == "all":
        # bosses = [boss.full_name_slug for boss in data.CURRENT_ZONE.bosses]
        bosses = [boss.full_name_slug for boss in RaidBoss.all]
    else:
        bosses = [boss_slug]

    # create tasks
    # for boss_slug in bosses:
    #     await api_tasks.create_cloud_function_task(
    #         function_name="load_comp_rankings",
    #         boss_slug=boss_slug,
    #         **kwargs
    #     )

    return {"message": "tasks queued", "bosses": bosses}
