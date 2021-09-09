"""Endpoints related to the Backend/API."""

# IMPORT STANDARD LIBRARIES
import datetime

# IMPORT THIRD PARTY LIBRARIES
import flask
from google.cloud import tasks_v2

# IMPORT LOCAL LIBRARIES
from lorgs import data
from lorgs.logger import logger
from lorgs.models import specs
from lorgs.models import warcraftlogs_ranking
from lorgs.models import warcraftlogs_comps


blueprint = flask.Blueprint("api", __name__, cli_group=None)



###############################################################################


@blueprint.get("/ping")
def ping():
    return {"reply": "Hi!", "time": datetime.datetime.utcnow().isoformat()}


###############################################################################
#
#       World Data
#
###############################################################################

@blueprint.get("/spell/<int:spell_id>")
def spell(spell_id):
    spell = specs.WowSpell.get(spell_id=spell_id)
    if not spell:
        flask.abort(404, description="Spell not found")
    return spell.as_dict()


@blueprint.get("/spells")
def spells():

    spells = specs.WowSpell.all

    # filter by group
    group = flask.request.args.get("group", default="", type=str)
    if group:
        spells = [spell for spell in spells if spell.group and spell.group.full_name_slug == group.lower()]

    return {spell.spell_id: spell.as_dict() for spell in spells}


###############################################################################
#
#       Spec Rankings
#
###############################################################################


@blueprint.route("/load_spec_rankings/<string:spec_slug>/<string:boss_slug>")
async def load_spec_rankings(spec_slug, boss_slug):
    limit = flask.request.args.get("limit", default=50, type=int)

    logger.info("START | spec=%s | boss=%s | limit=%d", spec_slug, boss_slug, limit)

    spec_ranking = warcraftlogs_ranking.SpecRanking.get_or_create(boss_slug=boss_slug, spec_slug=spec_slug)
    await spec_ranking.load(limit=limit)
    spec_ranking.save()

    logger.info("DONE | spec=%s | boss=%s | limit=%d", spec_slug, boss_slug, limit)
    return "done"


@blueprint.route("/spec_ranking/<string:spec_slug>/<string:boss_slug>")
def spec_ranking(spec_slug, boss_slug):
    spec_ranking = warcraftlogs_ranking.SpecRanking.get_or_create(boss_slug=boss_slug, spec_slug=spec_slug)
    players = [player.as_dict() for player in spec_ranking.players]

    return {
        "players": players,
    }


###############################################################################
#
#       Comps
#
###############################################################################

@blueprint.route("/comp_ranking/<string:name>")
def comp(name):
    comp = warcraftlogs_comps.CompConfig.objects(name=name).first()
    if not comp:
        flask.abort(404, description="Comp not found")

    return comp.as_dict()


@blueprint.route("/comp_ranking/<string:comp_name>/<string:boss_slug>")
def comp_ranking(comp_name, boss_slug):
    comp_ranking = warcraftlogs_comps.CompRating.get_or_create(comp=comp_name, boss_slug=boss_slug)
    return {
        "comp": comp_ranking.comp.name,
        "updated": comp_ranking.updated,
        "num_reports": len(comp_ranking.reports),
        "reports": [report.as_dict() for report in comp_ranking.reports]
    }

@blueprint.route("/load_comp_rankings/<string:comp_name>/<string:boss_slug>")
async def load_comp_rankings(comp_name, boss_slug):
    limit = flask.request.args.get("limit", default=50, type=int)

    comp_config = warcraftlogs_comps.CompConfig.objects(name=comp_name).first()

    scr = await comp_config.load_reports(boss_slug=boss_slug, limit=limit)
    scr.save()
    comp_config.save()

    return "done"


###############################################################################
#
#       Delayed Tasks
#
###############################################################################


def create_task(url, limit=0):
    google_task_client = tasks_v2.CloudTasksClient()
    parent = "projects/lorrgs/locations/europe-west2/queues/lorgs-task-queue"

    if limit:
        url += f"?limit={limit}"

    task = {
        "app_engine_http_request": {  # Specify the type of request.
            "http_method": tasks_v2.HttpMethod.GET,
            "relative_uri": url
        }
    }
    return google_task_client.create_task(request={"parent": parent, "task": task})


# LOAD SPECS

@blueprint.route("/task/load_spec_rankings/<string:spec_slug>")
async def task_load_spec_rankings_all_bosses(spec_slug):
    limit = flask.request.args.get("limit", default=0, type=int)

    for boss in data.SANCTUM_OF_DOMINATION_BOSSES:
        url = f"/api/task/load_spec_rankings/{spec_slug}/{boss.name_slug}"
        create_task(url, limit=limit)

    return "task queued"


@blueprint.route("/task/load_spec_rankings/<string:spec_slug>/<string:boss_slug>")
async def task_load_spec_rankings(spec_slug, boss_slug):

    limit = flask.request.args.get("limit", default=0, type=int)
    url = f"/api/load_spec_rankings/{spec_slug}/{boss_slug}"
    create_task(url, limit=limit)
    return "task queued"


# LOAD COMP

@blueprint.route("/task/load_comp_rankings/<string:comp_name>/<string:boss_slug>")
async def task_load_comp_rankings(comp_name, boss_slug):
    limit = flask.request.args.get("limit", default=0, type=int)

    url = f"/api/load_comp_rankings/{comp_name}/{boss_slug}"
    create_task(url, limit=limit)
    return "task queued"


@blueprint.route("/task/load_comp_rankings/<string:comp_name>")
async def task_load_comp_rankings_all(comp_name):
    limit = flask.request.args.get("limit", default=0, type=int)

    for boss in data.SANCTUM_OF_DOMINATION_BOSSES:
        url = f"/api/task/load_comp_rankings/{comp_name}/{boss.name_slug}"
        create_task(url, limit=limit)
    return "task queued"


# LOAD ALL


@blueprint.route("/task/load_all/specs")
async def task_load_all_specs():
    limit = flask.request.args.get("limit", default=0, type=int)
    for spec in data.SUPPORTED_SPECS:
        url = f"/api/task/load_spec_rankings/{spec.full_name_slug}"
        create_task(url, limit=limit)
    return "ok"


@blueprint.route("/task/load_all/comps")
async def task_load_all_comps():
    limit = flask.request.args.get("limit", default=0, type=int)
    comps = warcraftlogs_comps.CompConfig.objects
    for comp in comps:
        url = f"/api/task/load_comp_rankings/{comp.name}"
        create_task(url, limit=limit)
    return "ok"


@blueprint.route("/task/load_all")
async def task_load_all():
    limit = flask.request.args.get("limit", default=0, type=int)

    create_task("/api/task/load_all/specs", limit=limit)
    create_task("/api/task/load_all/comps", limit=limit)
    return "ok"
