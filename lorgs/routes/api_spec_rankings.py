# IMPORT STANDARD LIBRARIES
import json

# IMPORT THIRD PARTY LIBRARIES
import flask

# IMPORT LOCAL LIBRARIES
from lorgs import data
from lorgs.cache import cache
from lorgs.logger import logger
from lorgs.models import warcraftlogs_ranking
from lorgs.routes import api_tasks



blueprint = flask.Blueprint("api.spec_rankings", __name__)


@blueprint.route("/spec_ranking/<string:spec_slug>/<string:boss_slug>")
@cache.cached(query_string=True)
def spec_ranking(spec_slug, boss_slug):
    limit = flask.request.args.get("limit", default=0, type=int)

    spec_ranking = warcraftlogs_ranking.SpecRanking.get_or_create(boss_slug=boss_slug, spec_slug=spec_slug)
    fights = spec_ranking.fights

    if limit:
        fights = spec_ranking.fights[:limit]

    return {
        "fights": [fight.as_dict() for fight in fights],
    }


@blueprint.route("/load_spec_ranking/<string:spec_slug>/<string:boss_slug>")
async def load_spec_ranking(spec_slug, boss_slug):
    limit = flask.request.args.get("limit", default=50, type=int)
    clear = flask.request.args.get("clear", default=False, type=json.loads)

    logger.info("START | spec=%s | boss=%s | limit=%d | clear=%s", spec_slug, boss_slug, limit, clear)

    spec_ranking = warcraftlogs_ranking.SpecRanking.get_or_create(boss_slug=boss_slug, spec_slug=spec_slug)
    await spec_ranking.load(limit=limit, clear_old=clear)
    spec_ranking.save()

    logger.info("DONE | spec=%s | boss=%s | limit=%d", spec_slug, boss_slug, limit)
    return "done"

################################################################################
# Tasks
#

@blueprint.route("/task/load_spec_ranking/<string:spec_slug>/<string:boss_slug>")
def task_load_spec_rankings(spec_slug, boss_slug):
    url = f"/api/load_spec_ranking/{spec_slug}/{boss_slug}"
    api_tasks.create_task(url)
    return "task queued"


@blueprint.route("/task/load_spec_ranking/<string:spec_slug>")
def task_load_spec_rankings_all_bosses(spec_slug):
    for boss in data.SANCTUM_OF_DOMINATION_BOSSES:
        url = f"/api/task/load_spec_ranking/{spec_slug}/{boss.full_name_slug}"
        api_tasks.create_task(url)

    return "task queued"


# LOAD ALL

@blueprint.route("/task/load_spec_ranking/all")
def task_load_all_specs():
    for spec in data.SUPPORTED_SPECS:
        url = f"/api/task/load_spec_ranking/{spec.full_name_slug}"
        api_tasks.create_task(url)
    return "ok"
