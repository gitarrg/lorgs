"""Views/Routes for the UI/Frontend."""

import re
import time
from collections import defaultdict

# IMPORT THIRD PARTY LIBS
from sqlalchemy.sql import func
import flask
import sqlalchemy as sa

# IMPORT LOCAL LIBS
from lorgs import db
from lorgs import forms
from lorgs.logger import logger
# from lorgs import models
from lorgs import tasks
from lorgs import utils
from lorgs.cache import Cache
from lorgs.models import encounters
from lorgs.models import specs
# from lorgs.models import warcraftlogs
from lorgs.models import warcraftlogs_ranking


DEFAULT_BOSS_ID = 2407 # Sire Denathrius


def spec_ranking_color(i):
    if i == 1:
        return "text-artifact"
    if i <= 25:
        return "text-astounding"
    if i <= 100:
        return "text-legendary"
    return "text-epic"



BP = flask.Blueprint(
    "ui",
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="/"
)


SHARED_DATA = {}


@BP.app_context_processor
def add_shared_variables():
    config = flask.current_app.config
    return {
        # "wow_data": wow_data,
        "GOOGLE_ANALYTICS_ID": config["GOOGLE_ANALYTICS_ID"],
        "spec_ranking_color": spec_ranking_color,
    }


@BP.before_app_first_request
def load_shared_data():

    roles = specs.WowRole.query
    roles = roles.filter(specs.WowRole.id < 1000)
    roles = roles.options(sa.orm.joinedload(specs.WowRole.specs))
    roles = roles.all()
    SHARED_DATA["roles"] = roles
    SHARED_DATA["specs"] = utils.flatten(role.specs for role in roles)

    bosses = encounters.RaidBoss.query
    bosses = bosses.options(sa.orm.joinedload(encounters.RaidBoss.zone))
    bosses = bosses.all()
    SHARED_DATA["bosses"] = bosses


################################################################################
#
#   GLOBAL
#
################################################################################


@BP.route("/")
def index():
    """Render the main index page."""
    # query some data
    roles = specs.WowRole.query
    roles = roles.filter(specs.WowRole.id < 1000)
    roles = roles.options(sa.orm.joinedload(specs.WowRole.specs))
    roles = roles.all()
    boss = encounters.RaidBoss.query.get(DEFAULT_BOSS_ID)

    # render our template
    kwargs = {}
    kwargs["boss"] = boss
    kwargs["roles"] = roles
    return flask.render_template("index.html", **kwargs)


################################################################################
#
#   SPEC RANKINGS
#
################################################################################

@BP.route("/spec_ranking/<int:spec_id>/<int:boss_id>")
def spec_ranking(spec_id, boss_id):

    logger.info("spec_ranking 1")
    t1 = time.time()

    # Inputs
    spec = specs.WowSpec.query.get(spec_id)
    boss = encounters.RaidBoss.query.get(boss_id)
    if not (spec and boss):
        # TODO: add proper error message
        return {
            "spec": {"slug:": spec_id, "str": str(spec)},
            "boss": {"slug:": boss_id, "str": str(boss)},
        }
    t2 = time.time()
    logger.info("spec_ranking | Q1: %6.02f", (t2-t1)*1000)


    ranked_chars = warcraftlogs_ranking.RankedCharacter.query
    ranked_chars = ranked_chars.filter_by(spec_id=spec_id, boss_id=boss_id)
    ranked_chars = ranked_chars.order_by(warcraftlogs_ranking.RankedCharacter.amount.desc())
    ranked_chars = ranked_chars.limit(50)
    ranked_chars = ranked_chars.options(
        sa.orm.joinedload("spec"),
        sa.orm.joinedload("spec.wow_class"),
        sa.orm.joinedload("casts"),
        sa.orm.joinedload("casts.spell"),
    )
    ranked_chars = ranked_chars.all()

    t3 = time.time()
    logger.info("spec_ranking | Q1: %6.02f", (t3-t2)*1000)

    # preprocess some data
    spells_used = utils.flatten(char.spells_used for char in ranked_chars)
    spells_used = utils.uniqify(spells_used, key=lambda spell: spell)
    timeline_duration = max(char.fight_duration for char in ranked_chars) if ranked_chars else 0

    # Return
    kwargs = {}
    kwargs["spec"] = spec
    kwargs["boss"] = boss
    kwargs["players"] = ranked_chars
    kwargs["all_spells"] = spells_used
    kwargs["timeline_duration"] = timeline_duration
    return flask.render_template("spec_ranking.html", **kwargs, **SHARED_DATA)


################################################################################
#
#   REPORTS
#
################################################################################


@BP.route("/report", methods=['GET', 'POST'])
def report_index():
    form = forms.CustomReportForm()
    if form.validate_on_submit():
        link = form.report_link.data
        match = re.match(forms.WCL_LINK_REGEX, link)
        report_id = match.group("code")

        report_data = Cache.get(f"report/{report_id}")
        if not report_data:
            return flask.redirect(flask.url_for("ui.report_load", report_id=report_id))
        return flask.redirect(flask.url_for("ui.report", report_id=report_id))

    kwargs = {}
    kwargs["form"] = form
    return flask.render_template("report_index.html", **kwargs)


@BP.route("/report_load/<string:report_id>")
def report_load(report_id):
    task = tasks.load_report.delay(report_id=report_id)
    kwargs = {}
    kwargs["report_id"] = report_id
    kwargs["task_id"] = task.id
    return flask.render_template("report_loading.html", **kwargs)


@BP.route("/report/<string:report_id>")
def report(report_id):


    report = warcraftlogs.Report.query
    report = report.options(
        sa.orm.joinedload(warcraftlogs.Report.fights),
        sa.orm.joinedload("fights.boss"),
        sa.orm.joinedload("fights.players"),
        sa.orm.joinedload("fights.players.spec"),
        sa.orm.joinedload("fights.players.casts"),
        sa.orm.joinedload("fights.players.casts.spell"),
        # db.joinedload("fights.players.casts.player"),
        # db.joinedload("fights.players.casts.player.fight"),
    )
    report = report.get(report_id)
    if not report:
        return flask.redirect(flask.url_for("ui.report_load", report_id=report_id))

    bosses = encounters.RaidBoss.query.filter_by(zone_id=report.zone_id).all()

    all_players = utils.flatten([fight.players for fight in report.fights])

    specs = [player.spec for player in all_players]
    specs = list(set(specs))

    # TODO: check which spells are actually used
    used_spells = [(spec, spec.spells) for spec in specs]
    used_spells = sorted(used_spells)
    # used_spells = utils.uniqify(used_spells, key=lambda spell: (spell.group, spell.spell_id))

    kwargs = {
        "report": report,
        "all_spells": used_spells,
        "timeline_duration": max(f.duration for f in report.fights) if report.fights else 0,

        # Data for Nav
        # "roles": [],
        # "bosses": bosses
    }
    return flask.render_template("report.html", **kwargs)
