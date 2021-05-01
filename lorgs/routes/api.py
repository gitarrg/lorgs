"""Endpoints related to the Backend/API."""

# IMPORT STANDARD LIBRARIES
import asyncio

# IMPORT THIRD PARTY LIBRARIES
import flask

# IMPORT LOCAL LIBRARIES
from lorgs.cache import Cache
from lorgs.data import SPELLS
from lorgs import data
from lorgs.models import loader
from lorgs.models import Report
from lorgs.logger import logger
from lorgs import models
from lorgs import tasks


BP = flask.Blueprint("api", __name__, cli_group=None)


def _load_spells():
    logger.info("%d spells", len(SPELLS))
    data = asyncio.run(loader.load_spell_icons(SPELLS))

    # save cache
    spell_infos = [info for info in data.values()]
    Cache.set("spell_infos", spell_infos)

    spell_info_by_id = {info.pop("id"): info for info in spell_infos}

    # attach data to spells
    for spell in models.WowSpell.all:
        spell_info = spell_info_by_id.get(spell.spell_id, {})
        if not spell_info:
            logger.warning("No Spell Info for: %s", spell.spell_id)
            continue

        # check for existing values so we keep manual overwrites
        spell.spell_name = spell.spell_name or spell_info.get("name")
        spell.icon_name = spell.icon_name or spell_info.get("icon")

    logger.info("[load spell icons] done")


@BP.cli.command("load_spell_icons")
def load_spell_icons():
    _load_spells()


@BP.route("/load_spells")
def load_spells():
    _load_spells()
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


@BP.route("/load_report/<string:report_id>")
def load_report(report_id):

    report = Report(report_id=report_id)

    # TODO: replace with celery
    asyncio.run(loader.load_report(report))

    report = Cache.set(f"report/{report_id}", report, timeout=0)
    return {"message": "loaded"}


@BP.route("/task_load_report/<string:report_id>")
def task_load_report(report_id):
    logger.info("report_id: %s | START")
    tasks.load_report.delay("6YGnLdrtyKMWwcmx")
    logger.info("report_id: %s | DONE")
    return "ok"


@BP.route("/load_spec_rankings/<string:spec_full_name_slug>")
def load_spec_rankings(spec_full_name_slug):

    print("load_spec_rankings route", spec_full_name_slug)

    task_ids = []
    for boss in data.BOSSES:
        new_task = tasks.load_spec_ranking.delay(boss_id=boss.id, spec_full_name_slug=spec_full_name_slug, limit=50)
        task_ids += [new_task.id]

    return {"tasks": task_ids}


@BP.route("/task_test")
def task_test():
    import os
    logger.info("start | DONE")

    c = os.getenv("REDIS_HOST") or "localhostCACHE"
    logger.info("CACHE: %s", c)

    CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL", "redis://localhostCEL:6379")
    logger.info("CELERY: %s", CELERY_BROKER_URL)

    logger.info("CELERY: %s", os.environ)


    tasks.create_task.delay("x")
    logger.info("test | DONE")
    return "ok"
