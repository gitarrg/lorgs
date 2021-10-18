# IMPORT STANDARD LIBRARIES
import json

# IMPORT THIRD PARTY LIBRARIES
import flask

# IMPORT LOCAL LIBRARIES
from lorgs import data
from lorgs.cache import cache
from lorgs.logger import logger
from lorgs.models import warcraftlogs_ranking
from lorgs.models.wow_spec import WowSpec
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
        "updated": int(spec_ranking.updated.timestamp()),
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


@blueprint.route("/status/spec_ranking")
def status():

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

@blueprint.route("/task/load_spec_ranking/<string:spec_slug>/<string:boss_slug>")
def task_load_spec_rankings(spec_slug="", boss_slug=""):

    if spec_slug == "all":
        specs = [spec.full_name_slug for spec in WowSpec.all if spec.role.id < 1000] # filter out "other" and "boss"
    else:
        specs = [spec_slug]

    # Use the bossname given, or fall back to all bosses of the current zone
    if boss_slug == "all":
        bosses = [boss.full_name_slug for boss in data.CURRENT_ZONE.bosses]
    else:
        bosses = [boss_slug]

    # create the tasks
    for spec_slug in specs:
        for boss_slug in bosses:
            url = f"/api/load_spec_ranking/{spec_slug}/{boss_slug}"
            api_tasks.create_task(url)

    # return some status info
    return {
        "message": "tasks queued",
        "num_tasks": len(specs)*len(bosses),
        "specs": specs,
        "bosses": bosses,
    }
