"""Endpoints related to the Backend/API.

TODO:
    split this into a few files: world_data, specs, comp, tasks

"""

# IMPORT STANDARD LIBRARIES
import datetime
import urllib
import json

# IMPORT THIRD PARTY LIBRARIES
import flask
from google.cloud import tasks_v2

# IMPORT LOCAL LIBRARIES
from lorgs import data
from lorgs import utils
from lorgs.cache import cache
from lorgs.logger import logger
from lorgs.models import encounters, specs
from lorgs.models import warcraftlogs_ranking
from lorgs.models import warcraftlogs_comp_ranking


blueprint = flask.Blueprint("api", __name__, cli_group=None)


###############################################################################


@blueprint.route("/<path:path>")
def page_not_found(path):
    return "Invalid Route", 404


@blueprint.get("/ping")
def ping():
    return {"reply": "Hi!", "time": datetime.datetime.utcnow().isoformat()}


###############################################################################
#
#       World Data
#
###############################################################################

@blueprint.get("/roles")
@cache.cached()
def get_roles():
    return flask.jsonify({
        "roles": [role.as_dict() for role in specs.WowRole.all]
    })
    return {}
       
    


@blueprint.get("/spells/<int:spell_id>")
@cache.cached()
def spells_one(spell_id):
    spell = specs.WowSpell.get(spell_id=spell_id)
    if not spell:
        flask.abort(404, description="Spell not found")
    return spell.as_dict()


@blueprint.get("/spells")
@cache.cached(query_string=True)
def spells_all():

    spells = specs.WowSpell.all

    # filter by group
    groups = flask.request.args.getlist("group") #, default="", type=str)
    if groups:
        spells = [spell for spell in spells if spell.group and spell.group.full_name_slug in groups]

    return {spell.spell_id: spell.as_dict() for spell in spells}


@blueprint.get("/specs")
@cache.cached(query_string=True)
def get_specs_all():
    include_spells = flask.request.args.get("include_spells", default=False, type=json.loads)

    all_specs = sorted(specs.WowSpec.all)
    all_specs = [specs.as_dict(spells=include_spells) for specs in all_specs]
    return {"specs": all_specs}


@blueprint.get("/specs/<string:spec_slug>")
@cache.cached(query_string=True)
def get_spec(spec_slug):
    spec = specs.WowSpec.get(full_name_slug=spec_slug)
    if not spec:
        return "Invalid Spec.", 404
    return spec.as_dict()


@blueprint.get("/bosses")
@blueprint.get("/zone/bosses")
@blueprint.get("/zone/<int:zone_id>/bosses")
@cache.cached()
def get_bosses(zone_id=28):
    zone = encounters.RaidZone.get(id=zone_id)
    if not zone:
        return "Invalid Zone.", 404
    return zone.as_dict()


@blueprint.get("/boss/<string:boss_slug>")
@cache.cached()
def get_boss(boss_slug):
    include_spells = flask.request.args.get("include_spells", default=True, type=json.loads)
    boss = encounters.RaidBoss.get(full_name_slug=boss_slug)
    if not boss:
        return "Invalid Boss.", 404
    return boss.as_dict(include_spells=include_spells)



###############################################################################
#
#       Spec Rankings
#
###############################################################################

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


@blueprint.route("/load_spec_rankings/<string:spec_slug>/<string:boss_slug>")
async def load_spec_rankings(spec_slug, boss_slug):
    limit = flask.request.args.get("limit", default=50, type=int)
    clear = flask.request.args.get("clear", default=False, type=json.loads)

    logger.info("START | spec=%s | boss=%s | limit=%d | clear=%s", spec_slug, boss_slug, limit, clear)

    spec_ranking = warcraftlogs_ranking.SpecRanking.get_or_create(boss_slug=boss_slug, spec_slug=spec_slug)
    await spec_ranking.load(limit=limit, clear_old=clear)
    spec_ranking.save()

    logger.info("DONE | spec=%s | boss=%s | limit=%d", spec_slug, boss_slug, limit)
    return "done"


###############################################################################
#
#       Comps
#
###############################################################################

"""
@blueprint.route("/comp_ranking/<string:name>")
def comp(name):
    comp = warcraftlogs_comps.CompConfig.objects(name=name).first()
    if not comp:
        flask.abort(404, description="Comp not found")
    return comp.as_dict()
"""


@blueprint.route("/comp_ranking/<string:boss_slug>")
def comp_ranking(boss_slug):
    limit = flask.request.args.get("limit", default=50, type=int)

    comp_ranking = warcraftlogs_comp_ranking.CompRanking(boss_slug=boss_slug)
    reports = comp_ranking.get_reports(limit=limit)

    # DEV LIMIT
    for r in reports:
        r.fight.players = r.fight.players[:20]

    return {
        "fights": [report.fight.as_dict() for report in reports if report.fight],
        "updated": comp_ranking.updated,
    }


@blueprint.route("/load_comp_rankings/<string:comp_name>/<string:boss_slug>")
async def load_comp_rankings(comp_name, boss_slug):
    limit = flask.request.args.get("limit", default=50, type=int)
    clear = flask.request.args.get("clear", default=False, type=json.loads)

    comp_config = warcraftlogs_comps.CompConfig.objects(name=comp_name).first()

    scr = await comp_config.load_reports(boss_slug=boss_slug, limit=limit, clear_old=clear)
    scr.save()
    comp_config.save()

    return "done"


###############################################################################
#
#       Delayed Tasks
#
###############################################################################


def create_task(url):
    google_task_client = tasks_v2.CloudTasksClient()
    parent = "projects/lorrgs/locations/europe-west2/queues/lorgs-task-queue"

    if flask.request.args:
        url += "?" + urllib.parse.urlencode(flask.request.args)

    task = {
        "app_engine_http_request": {  # Specify the type of request.
            "http_method": tasks_v2.HttpMethod.GET,
            "relative_uri": url
        }
    }
    return google_task_client.create_task(request={"parent": parent, "task": task})


# LOAD SPECS

@blueprint.route("/task/load_spec_rankings/<string:spec_slug>/<string:boss_slug>")
async def task_load_spec_rankings(spec_slug, boss_slug):
    url = f"/api/load_spec_rankings/{spec_slug}/{boss_slug}"
    create_task(url)
    return "task queued"


@blueprint.route("/task/load_spec_rankings/<string:spec_slug>")
async def task_load_spec_rankings_all_bosses(spec_slug):
    for boss in data.SANCTUM_OF_DOMINATION_BOSSES:
        url = f"/api/task/load_spec_rankings/{spec_slug}/{boss.name_slug}"
        create_task(url)

    return "task queued"


# LOAD COMP

@blueprint.route("/task/load_comp_rankings/<string:comp_name>/<string:boss_slug>")
async def task_load_comp_rankings(comp_name, boss_slug):
    url = f"/api/load_comp_rankings/{comp_name}/{boss_slug}"
    create_task(url)
    return "task queued"


@blueprint.route("/task/load_comp_rankings/<string:comp_name>")
async def task_load_comp_rankings_all(comp_name):
    for boss in data.SANCTUM_OF_DOMINATION_BOSSES:
        url = f"/api/task/load_comp_rankings/{comp_name}/{boss.name_slug}"
        create_task(url)
    return "task queued"


# LOAD ALL

@blueprint.route("/task/load_all/specs")
async def task_load_all_specs():
    for spec in data.SUPPORTED_SPECS:
        url = f"/api/task/load_spec_rankings/{spec.full_name_slug}"
        create_task(url)
    return "ok"


@blueprint.route("/task/load_all/comps")
async def task_load_all_comps():
    comps = warcraftlogs_comps.CompConfig.objects
    for comp in comps:
        url = f"/api/task/load_comp_rankings/{comp.name}"
        create_task(url)
    return "ok"


@blueprint.route("/task/load_all")
async def task_load_all():
    create_task("/api/task/load_all/specs")
    create_task("/api/task/load_all/comps")
    return "ok"
