"""API Routes to get and update Comp Rankings."""

# IMPORT STANDARD LIBRARIES
import typing

# IMPORT THIRD PARTY LIBRARIES
import fastapi

# IMPORT LOCAL LIBRARIES
from lorgs import data
from lorgs.models.raid_boss import RaidBoss
from lorgs.models import warcraftlogs_comp_ranking
from lorrgs_api.routes import api_tasks


router = fastapi.APIRouter()



@router.get("/comp_ranking/{boss_slug}")
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

    search["fights.0"] = []
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
