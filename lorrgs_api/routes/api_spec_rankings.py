# IMPORT THIRD PARTY LIBRARIES
import fastapi

# IMPORT LOCAL LIBRARIES
from lorgs import data
from lorgs.logger import logger
from lorgs.models import warcraftlogs_ranking
from lorgs.models.task import Task
from lorgs.models.wow_spec import WowSpec
from lorgs.models.raid_boss import RaidBoss
# from lorrgs_api.routes import api_tasks


router = fastapi.APIRouter(tags=["spec_rankings"])


@router.get("/spec_ranking/{spec_slug}/{boss_slug}")
async def get_spec_ranking(
    spec_slug,
    boss_slug,
    difficulty: str = "mythic",
    metric: str = "",
    limit: int = 0
):
    if not metric:
        spec = WowSpec.get(full_name_slug=spec_slug)
        metric = spec.role.metric

    spec_ranking = warcraftlogs_ranking.SpecRanking.get_or_create(
        boss_slug=boss_slug,
        spec_slug=spec_slug,
        difficulty=difficulty,
        metric=metric,
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
        "difficulty": difficulty,
        "metric": metric,
    }


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

@router.get("/spec_ranking/load")
async def spec_ranking_load(
    spec_slug="all", boss_slug="all",
    difficulty="all", metric="all",
    limit: int = 50, clear: bool = False
):
    payload = {
        "task": "load_spec_rankings",
        "spec_slug": spec_slug, "boss_slug": boss_slug,
        "difficulty": difficulty, "metric": metric,
        "limit": limit, "clear": clear,
    }
    task = Task.submit(payload=payload, save=False)

    return {
        "message": "task queued",
        "task": task.task_id,
        "payload": payload
    }
