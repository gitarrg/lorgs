"""Views/Routes for the UI/Frontend."""


import re

# IMPORT THIRD PARTY LIBS
import flask

# IMPORT LOCAL LIBS
# from lorgs import db
from lorgs import forms
# from lorgs.logger import logger
# from lorgs import models
# from lorgs import tasks
from lorgs import data
from lorgs import utils
# from lorgs.cache import Cache
# from lorgs.models import encounters
# from lorgs.models import specs
# from lorgs.models import warcraftlogs
from lorgs.models import warcraftlogs_ranking
from lorgs.models import warcraftlogs_comps
# from lorgs.models import warcraftlogs_base
from lorgs.models import warcraftlogs_report


blueprint = flask.Blueprint(
    "ui",
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="/"
)


SHARED_DATA = {}


@blueprint.app_context_processor
def add_shared_variables():
    config = flask.current_app.config
    return {
        # "wow_data": wow_data,
        "GOOGLE_ANALYTICS_ID": config["GOOGLE_ANALYTICS_ID"],
    }


################################################################################
#
#   GLOBAL
#
################################################################################

@blueprint.errorhandler(404)
async def page_not_found(error):
    # note that we set the 404 status explicitly
    return flask.render_template("errors/404.html", error=error), 404


@blueprint.get("/")
async def index():
    """Render the main index page."""
    kwargs = {}
    kwargs["boss"] = data.DEFAULT_BOSS
    kwargs["roles"] = data.ROLES
    kwargs["comps"] = warcraftlogs_comps.CompConfig.objects
    return flask.render_template("index.html", **kwargs)


################################################################################
#
#   SPEC RANKINGS
#
################################################################################

@blueprint.route("/spec_ranking/<string:spec_slug>/<string:boss_slug>")
async def spec_ranking(spec_slug, boss_slug):

    # Inputs
    # limit = flask.request.args.get("limit", default=50, type=int)
    spec_ranking = warcraftlogs_ranking.SpecRanking.objects(boss_slug=boss_slug, spec_slug=spec_slug).first()
    if not spec_ranking:
        flask.abort(404, description="Invalid Spec or Boss")

    # preprocess some data
    spells_used = utils.flatten(player.spells_used for player in spec_ranking.players)
    spells_used = utils.uniqify(spells_used, key=lambda spell: spell)
    timeline_duration = max(fight.duration for fight in spec_ranking.fights) if spec_ranking.fights else 0


    boss_player = None
    for fight in spec_ranking.fights:
        if fight.boss and fight.boss.casts:
            boss_player = fight.boss
            break

    # Return
    kwargs = {}
    kwargs["spec"] = spec_ranking.spec
    kwargs["boss"] = spec_ranking.boss

    kwargs["players"] = spec_ranking.players
    kwargs["boss_player"] = boss_player
    kwargs["all_spells"] = spells_used
    kwargs["timeline_duration"] = timeline_duration

    kwargs["roles"] = data.ROLES
    kwargs["bosses"] = spec_ranking.boss.zone.bosses

    return flask.render_template("spec_ranking.html", **kwargs)

################################################################################
#
#   COMPS
#
################################################################################


@blueprint.route("/comp_ranking/<string:comp_name>/<string:boss_slug>")
async def comp_ranking(comp_name, boss_slug):
    comp_ranking = warcraftlogs_comps.CompRating.get_or_create(comp=comp_name, boss_slug=boss_slug)

    kwargs = {}
    kwargs["comp_ranking"] = comp_ranking
    kwargs["all_spells"] = comp_ranking.spells_used
    kwargs["timeline_duration"] = max(fight.duration for fight in comp_ranking.fights) if comp_ranking.fights else 0

    kwargs["roles"] = data.ROLES
    kwargs["bosses"] = data.CASTLE_NATHRIA.bosses

    return flask.render_template("comp_ranking.html", **kwargs)


################################################################################
#
#   REPORTS
#
################################################################################

@blueprint.route("/report", methods=['GET', 'POST'])
@blueprint.route("/reports", methods=['GET', 'POST'])
async def report_index():
    form = forms.CustomReportForm()
    if form.validate_on_submit():
        link = form.report_link.data
        match = re.match(forms.WCL_LINK_REGEX, link)
        report_id = match.group("code")

        user_report = warcraftlogs_report.UserReport.get_or_create(report_id=report_id)
        # report_data = Cache.get(f"report/{report_id}")
        # if not report_data:
        #     return flask.redirect(flask.url_for("ui.report_load", report_id=report_id))
        return flask.redirect(flask.url_for("ui.report", report_id=report_id))

    kwargs = {}
    kwargs["form"] = form
    return flask.render_template("report_index.html", **kwargs)


'''
@blueprint.route("/report_load/<string:report_id>")
def report_load(report_id):
    task = tasks.load_report.delay(report_id=report_id)
    kwargs = {}
    kwargs["report_id"] = report_id
    kwargs["task_id"] = task.id
    return flask.render_template("report_loading.html", **kwargs)
'''


@blueprint.route("/report/<string:report_id>")
async def report(report_id):

    user_report = warcraftlogs_report.UserReport.objects(report__report_id=report_id).first()
    # user_report = warcraftlogs_report.UserReport.get_or_create(report_id=report_id)

    if not user_report:
        flask.abort(404, description="Report not found")
        # return flask.redirect(flask.url_for("ui.report_load", report_id=report_id))

    report = user_report.report

    players = utils.uniqify(report.players, key=lambda player: player.source_id)
    spells_used = utils.flatten(player.spells_used for player in players)
    spells_used = utils.uniqify(spells_used, key=lambda spell: (spell.spell_id, spell.group))
    # used_spells = []

    boss = None
    for fight in report.fights:
        boss = fight.boss.raid_boss
        break

    kwargs = {
        "report": report,
        "boss": boss,

        "unique_players": players,
        "all_spells": spells_used,
        # "timeline_duration": max(f.duration for f in report.fights) if report.fights else 0,
    }
    return flask.render_template("report.html", **kwargs)
