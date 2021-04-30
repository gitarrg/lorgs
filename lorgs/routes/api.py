"""Endpoints related to the Backend/API."""

# IMPORT STANDARD LIBRARIES
import asyncio

# IMPORT THIRD PARTY LIBRARIES
import flask

# IMPORT LOCAL LIBRARIES
from lorgs.cache import Cache
from lorgs.data import SPELLS
from lorgs.models import loader
from lorgs.models import Report
from lorgs.logger import logger
from lorgs import models


BP = flask.Blueprint("api", __name__, cli_group=None)


def _load_spells():
    logger.info("%d spells", len(SPELLS))
    data = asyncio.run(loader.load_spell_icons(SPELLS))

    # save cache
    spell_infos = {info.pop("id"): info for info in data.values()}
    Cache.set("spell_infos", spell_infos, timeout=0)

    # attach data to spells
    for spell in models.WowSpell.all:
        spell_info = spell_infos.get(spell.spell_id, {})
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
    return {spell.spell_id: spell.as_dict() for spell in SPELLS}


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



