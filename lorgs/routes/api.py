"""Endpoints related to the Backend/API."""

# IMPORT STANDARD LIBRARIES
# import asyncio
import os

# IMPORT THIRD PARTY LIBRARIES
import flask
from celery.result import AsyncResult

# IMPORT LOCAL LIBRARIES
# from lorgs.models import loader
from lorgs import data
from lorgs import tasks
from lorgs.cache import Cache
from lorgs.logger import logger
from lorgs.models import Report



BP = flask.Blueprint("api", __name__, cli_group=None)


@BP.cli.command("load_spell_icons")
def load_spell_icons():
    raise NotImplementedError


@BP.route("/load_spells")
def load_spells():
    tasks.load_spell_icons.delay()
    return "ok"


@BP.route("/spells")
def spells():
    return {spell.spell_id: spell.as_dict() for spell in data.SPELLS}


@BP.route("/report/<string:report_id>")
def report(report_id):

    report = Cache.get(f"report/{report_id}")
    if not report:
        return {"error": "not found"}

    return report.as_dict()


"""
@BP.route("/load_report/<string:report_id>")
def load_report(report_id):

    report = Report(report_id=report_id)
    # TODO: replace with celery
    # asyncio.run(loader.load_report(report))

    Cache.set(f"report/{report_id}", report, timeout=0)
    return {"message": "loaded"}
"""

@BP.route("/load_report/<string:report_id>")
def task_load_report(report_id=""):
    report_id = report_id or "6YGnLdrtyKMWwcmx"
    logger.info("report_id: %s | START", report_id)

    task = tasks.load_report.delay(report_id)
    return {
        "task": task.id
    }


@BP.route("/task_status/<string:task_id>")
def task_status(task_id):
    task = AsyncResult(task_id)
    logger.info("task: %s", task.result)
    # logger.info("STATUS: %s", task.status)

    info = task.info or {}
    if task.failed:
        info = {} # as the Exception might not be JSON serializable

    return {
        "status": task.status,
        "info": info,
    }



@BP.route("/load_spec_rankings/<string:spec_full_name_slug>/<int:boss_id>")
def load_spec_rankings(spec_full_name_slug, boss_id):

    print("load_spec_rankings route", spec_full_name_slug, boss_id)

    # task_ids = []
    # for boss in data.BOSSES:
    limit = 10 if os.getenv("DEBUG") else 50
    new_task = tasks.load_spec_ranking.delay(boss_id=boss_id, spec_full_name_slug=spec_full_name_slug, limit=limit)
    """
    """
    # task_ids += [new_task.id]
    # return {"tasks": task_ids}
    return {"task": new_task.id}


@BP.route("/test")
def test():
    import os
    test_value = Cache.get("test_value")

    return {
        "status": "OK",
        "value": test_value,

        "WCL_CLIENT_ID": os.getenv("WCL_CLIENT_ID", "not set")
    }


@BP.route("/task_debug")
def task_test():
    logger.info("start | DONE")

    for i in range(50):
        tasks.debug_task.delay(i)

    logger.info("test | DONE")
    return "ok"

