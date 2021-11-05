"""API Routes to get and update Comp Rankings."""

# IMPORT STANDARD LIBRARIES
import typing

# IMPORT THIRD PARTY LIBRARIES
import fastapi
from fastapi_cache.decorator import cache
from google.api_core import retry

# IMPORT LOCAL LIBRARIES
from lorgs import data
from lorgs.models import warcraftlogs_comp_ranking
from lorgs.routes import api_tasks


router = fastapi.APIRouter()



@router.get("/comp_ranking/{boss_slug}")
@cache()
async def get_comp_ranking(
        boss_slug: str,

        # Query Params
        limit: int = 20,
        role: typing.List[str] = fastapi.Query([""]),
        spec: typing.List[str] = fastapi.Query([""]),
        killtime_min: int=0,
        killtime_max: int=0,
):
    """Fetch comp rankings for a given boss encounter.

    Args:
        boss_slug (str): name of the boss (full_name_slug)

    Query Params:
        limit (int): max number of fights to fetch (default: 20)
        role (list[str]): role filters
        spec (list[str]): spec filters

    Returns:
        dict:
            fights (list[dict]):
            updated

    """
    # get search inputs
    search = {}
    search["fights.0.composition.roles"] = role or []
    search["fights.0.composition.specs"] = spec or []
    search["fights.0.composition.classes"] = []  # implement this, if needed

    search["fights"] = []
    if killtime_min:
        search["fights.0"] += [f"duration.gt.{killtime_min * 1000}"]
    if killtime_max:
        search["fights.0"] += [f"duration.lt.{killtime_max * 1000}"]

    # lookup DB
    comp_ranking = warcraftlogs_comp_ranking.CompRanking(boss_slug=boss_slug)
    if not comp_ranking.valid:
        return "Invalid Boss.", 404

    reports = comp_ranking.get_reports(limit=limit, search=search)

    # return
    return {
        "fights": [report.fight.as_dict() for report in reports if report.fight],
        "updated": comp_ranking.updated,
    }


@router.get("/load_comp_ranking/{boss_slug}")
async def load_comp_ranking(boss_slug: str, limit: int = 50, clear: bool = False):
    """Load Comp Rankings from Warcraftlogs and save them in our DB.

    Args:
        boss_slug (str): name of the boss (full_name_slug)

    Query Parms:
        limit (int): maximum number of fights to fetch (default: 100)
        clear (bool): delete old fights (default: false)

    """
    # get comp ranking object
    comp_ranking = warcraftlogs_comp_ranking.CompRanking(boss_slug=boss_slug)
    if not comp_ranking.valid:
        return "Invalid Boss.", 404

    # update
    await comp_ranking.update_reports(limit=limit, clear_old=clear)
    comp_ranking.save()

    return "done"


################################################################################
# Tasks
#
@router.get("/task/load_comp_ranking/{boss_slug}")
async def task_load_comp_rankings(boss_slug: str = "all", limit: int = 50, clear: bool = False):
    """Submit a scheduled task to update a single or all Comp Rankings."""
    kwargs = {"limit": limit, "clear": clear}

    # expand bosses
    if boss_slug == "all":
        bosses = [boss.full_name_slug for boss in data.CURRENT_ZONE.bosses]
    else:
        bosses = [boss_slug]

    # create tasks
    for boss_slug in bosses:
        api_tasks.create_cloud_function_task(
            function_name="load_comp_rankings",
            boss_slug=boss_slug,
            **kwargs
        )

    return {"message": "tasks queued", "bosses": bosses}
