"""Endpoints related to the Backend/API."""

# IMPORT STANDARD LIBRARIES
import asyncio
import datetime
import time

# IMPORT THIRD PARTY LIBRARIES
import flask
from google.cloud import tasks_v2

# IMPORT LOCAL LIBRARIES
from lorgs.logger import logger
from lorgs.models import specs
from lorgs.models import warcraftlogs_ranking
from lorgs.models import warcraftlogs_comps


blueprint = flask.Blueprint("api", __name__, cli_group=None)


###############################################################################

google_task_client = tasks_v2.CloudTasksClient()


def create_task(url, limit=None):
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


###############################################################################


@blueprint.route("/ping")
def ping():
    return {"reply": "Hi!", "time": datetime.datetime.utcnow().isoformat()}


@blueprint.route("/async_test/<int:n>")
async def async_test(n):
    """Quick Test for Async Performance on different webservers.

    >>> seq 100 | xargs -I %d -n 1 -P 999 curl http://localhost:5010/api/async_test/%d
    """
    # for i in range(10):
    print(f"async_test n={n} START")
    await asyncio.sleep(1)
    print(f"async_test n={n} DONE")

    return "ok", 200


@blueprint.route("/task_status/<string:task_id>")
def task_status(task_id):

    task = AsyncResult(task_id)
    info = task.info or {}
    if task.failed:
        info = {} # as the Exception might not be JSON serializable

    return {
        "status": task.status,
        "info": info,
    }


###############################################################################
#
#       World Data
#
###############################################################################

@blueprint.route("/spell/<int:spell_id>")
def spell(spell_id):
    spell = specs.WowSpell.get(spell_id=spell_id)
    if not spell:
        flask.abort(404, description="Spell not found")
    return spell.as_dict()


@blueprint.route("/spells")
def spells():
    return {spell.spell_id: spell.as_dict() for spell in specs.WowSpell.all}


###############################################################################
#
#       Spec Rankings
#
###############################################################################


@blueprint.route("/load_spec_rankings/<string:spec_slug>/<string:boss_slug>")
async def load_spec_rankings(spec_slug, boss_slug):
    limit = flask.request.args.get("limit", default=50, type=int)
    delayed = flask.request.args.get("delayed", default=False, type=bool)

    if delayed:
        create_task(f"/api/load_spec_rankings/{spec_slug}/{boss_slug}")
        return "task queued", 201

    spec_ranking = warcraftlogs_ranking.SpecRanking.get_or_create(boss_slug=boss_slug, spec_slug=spec_slug)
    await spec_ranking.load(limit=limit)
    spec_ranking.save()

    return "done"

    # new_task = tasks.load_spec_ranking.delay(boss_id=boss_id, spec_id=spec_id, limit=limit)
    # return {"task": new_task.id}


@blueprint.route("/spec_ranking/<string:spec_slug>/<string:boss_slug>")
def spec_ranking(spec_slug, boss_slug):

    # limit = flask.request.args.get("limit", default=50, type=int)

    t1 = time.time()

    # query them all into memory
    spec_ranking = warcraftlogs_ranking.SpecRanking.objects(boss_slug=boss_slug, spec_slug=spec_slug).first()
    spec_ranking = spec_ranking or warcraftlogs_ranking.SpecRanking(boss_slug=boss_slug, spec_slug=spec_slug)

    t2 = time.time()

    players = [player.as_dict() for player in spec_ranking.players]

    t21 = (t2-t1) * 1000

    return {
        "players": players,

        "times": {
            "t2-t1": f"{t21:.3}ms",
        }
    }


@blueprint.route("/spec_ranking_test/<string:spec_slug>/<string:boss_slug>")
def spec_ranking_test(spec_slug, boss_slug):
    count = flask.request.args.get("count", default=10, type=int)

    results = []
    for i in range(count):

        t1 = time.time()

        # query them all into memory
        spec_ranking = warcraftlogs_ranking.SpecRanking.objects(boss_slug=boss_slug, spec_slug=spec_slug).first()
        spec_ranking = spec_ranking or warcraftlogs_ranking.SpecRanking(boss_slug=boss_slug, spec_slug=spec_slug)

        t2 = time.time()
        results.append((t2-t1) * 1000)

    return {
        "results": results,
        "avg": sum(results) / count,
        "min": min(results),
        "max": max(results),
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

@blueprint.route("/load_comp_ranking/<string:comp_name>/<string:boss_slug>")
async def load_comp_ranking(comp_name, boss_slug):
    limit = flask.request.args.get("limit", default=50, type=int)

    comp_config = warcraftlogs_comps.CompConfig.objects(name=comp_name).first()

    scr = await comp_config.load_reports(boss_slug=boss_slug, limit=limit)
    scr.save()
    comp_config.save()

    return "done"


###############################################################################
#
#       Reports
#
###############################################################################

@blueprint.route("/load_report/<string:report_id>")
def load_report(report_id):
    logger.info("report_id: %s | START", report_id)
    task = tasks.load_report.delay(report_id)
    return {"task": task.id}

"""

@blueprint.route("/report/<string:report_id>")
def report(report_id):

    report = warcraftlogs_report.Report.query.get(report_id)
    if not report:
        flask.abort(404, description="Report not found")

    return report.as_dict()


@blueprint.route("/report/<string:report_id>/fight/<int:fight_id>")
def report_fight(report_id, fight_id):

    fight = warcraftlogs_report.Fight.query
    fight = fight.filter_by(report_id=report_id, fight_id=fight_id)
    fight = fight.first()

    if not fight:
        flask.abort(404, description="Fight not found")
    return fight.as_dict()


@blueprint.route("/report/<string:report_id>/fight/<int:fight_id>/player/<int:source_id>")
def report_fight_player(report_id, fight_id, source_id):

    player = warcraftlogs_report.Player.query
    player = player.filter_by(report_id=report_id, fight_id=fight_id, source_id=source_id)
    player = player.first()

    if not player:
        flask.abort(404, description="Fight not found")
    return player.as_dict()
"""