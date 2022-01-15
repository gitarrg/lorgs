# IMPORT THIRD PARTY LIBRARIES
import fastapi
from fastapi_cache.decorator import cache

# IMPORT LOCAL LIBRARIES
from lorgs import data
from lorgs.logger import logger
from lorgs.models import warcraftlogs_ranking
from lorgs.models.wow_spec import WowSpec
from lorgs.routes import api_tasks



router = fastapi.APIRouter(tags=["spec_rankings"])


@router.get("/spec_ranking/{spec_slug}/{boss_slug}")
@router.get("/spec_ranking/{spec_slug}/{boss_slug}/{difficulty}")
@cache()
async def get_spec_ranking(spec_slug, boss_slug, difficulty: str = "mythic", limit: int = 0):

    spec_ranking = warcraftlogs_ranking.SpecRanking.get_or_create(
        boss_slug=boss_slug,
        spec_slug=spec_slug,
        difficulty=difficulty,
    )
    fights = spec_ranking.fights or []

    if limit:
        fights = fights[:limit]

    # remove bosses
    for fight in fights[1:]:
        fight.boss = None


    return {
        "fights": [fight.as_dict() for fight in fights],
        "updated": int(spec_ranking.updated.timestamp()),
    }


@router.get("/load_spec_ranking/{spec_slug}/{boss_slug}")
async def load_spec_ranking(spec_slug, boss_slug, limit: int =50, clear: bool = False):
    logger.info("START | spec=%s | boss=%s | limit=%d | clear=%s", spec_slug, boss_slug, limit, clear)

    spec_ranking = warcraftlogs_ranking.SpecRanking.get_or_create(boss_slug=boss_slug, spec_slug=spec_slug)
    await spec_ranking.load(limit=limit, clear_old=clear)
    spec_ranking.save()

    logger.info("DONE | spec=%s | boss=%s | limit=%d", spec_slug, boss_slug, limit)
    return "done"


@router.get("/status/spec_ranking")
async def status():

    x = {}
    for sr in warcraftlogs_ranking.SpecRanking.objects().exclude("reports"):
        x[sr.spec_slug] = x.get(sr.spec_slug) or {}
        x[sr.spec_slug][sr.boss_slug] = {
            "updated": int(sr.updated.timestamp()),
        }

    return x


################################################################################
# Tasks
#

@router.get("/task/load_spec_ranking/{spec_slug}/{boss_slug}")
async def task_load_spec_rankings_multi(spec_slug="all", boss_slug="all", limit: int = 50, clear: bool = False):

    def message(specs, bosses):
        # return some status info
        return {
            "message": "tasks queued",
            "num_tasks": len(specs)*len(bosses),
            "specs": specs,
            "bosses": bosses,
        }

    kwargs = {"limit": limit, "clear": clear}

    # expand specs
    if spec_slug == "all":
        specs = [spec.full_name_slug for spec in WowSpec.all if spec.role.id < 1000] # filter out "other" and "boss"
        for spec_slug in specs:
            url = f"/api/task/load_spec_ranking/{spec_slug}/{boss_slug}"
            await api_tasks.create_app_engine_task(url, **kwargs)
        return message(specs, [boss_slug])

    # expand bosses
    if boss_slug == "all":
        bosses = [boss.full_name_slug for boss in data.CURRENT_ZONE.bosses]
        for boss_slug in bosses:
            url = f"/api/task/load_spec_ranking/{spec_slug}/{boss_slug}"
            await api_tasks.create_app_engine_task(url, **kwargs)
        return message([spec_slug], bosses)

    # create the actual task
    await api_tasks.create_cloud_function_task(
        function_name="load_spec_rankings",
        spec_slug=spec_slug,
        boss_slug=boss_slug,
        **kwargs
    )
    return message([spec_slug], [boss_slug])
