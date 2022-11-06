"""Enpoints dealing with Rankings per Spec."""
# IMPORT THIRD PARTY LIBRARIES
import fastapi

# IMPORT LOCAL LIBRARIES
from lorgs.clients import sqs
from lorgs.logger import logger
from lorgs.models import warcraftlogs_ranking
from lorgs.models.wow_spec import WowSpec


router = fastapi.APIRouter(tags=["spec_rankings"])


@router.get("/spec_ranking/{spec_slug}/{boss_slug}")
async def get_spec_ranking(
    spec_slug: str,
    boss_slug: str,
    difficulty: str = "mythic",
    metric: str = "",
):
    """Get the Rankings for a given Spec and Boss."""
    if not metric:
        spec = WowSpec.get(full_name_slug=spec_slug)
        metric = spec.role.metric

    logger.info(f"{spec_slug}/{boss_slug} | start")
    spec_ranking = warcraftlogs_ranking.SpecRanking.get(
        boss_slug=boss_slug,
        spec_slug=spec_slug,
        difficulty=difficulty,
        metric=metric,
        create=True,
    )
    return spec_ranking.dict(exclude_unset=True)


################################################################################
# Tasks
#


@router.get("/spec_ranking/load")
async def spec_ranking_load(
    spec_slug="all",
    boss_slug="all",
    difficulty="all",
    metric="all",
    limit: int = 50,
    clear: bool = False,
):
    """Queue an update for the given specs and bosses."""
    payload = {
        "task": "load_spec_rankings",
        "spec_slug": spec_slug,
        "boss_slug": boss_slug,
        "difficulty": difficulty,
        "metric": metric,
        "limit": limit,
        "clear": clear,
    }
    message = sqs.send_message(payload=payload)

    return {
        "message": "task queued",
        "task": message.get("MessageId"),
        "payload": payload,
    }
