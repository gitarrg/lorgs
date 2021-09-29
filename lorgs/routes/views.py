"""Views/Routes for the UI/Frontend."""

import re

# IMPORT THIRD PARTY LIBS
import flask

# IMPORT LOCAL LIBS
from lorgs import data
from lorgs import forms
from lorgs import utils
from lorgs.cache import cache
from lorgs.models import encounters
from lorgs.models import warcraftlogs_comps
from lorgs.models import warcraftlogs_report
from lorgs.models.specs import WowSpec


blueprint = flask.Blueprint(
    "ui",
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="/"
)


################################################################################
#
#   GLOBAL
#
################################################################################

@blueprint.app_errorhandler(404)
async def page_not_found(error):
    # note that we set the 404 status explicitly
    return flask.render_template("errors/404.html", error=error), 404


@blueprint.get("/")
@cache.cached()
def index():
    """Render the main index page."""
    kwargs = {}
    kwargs["boss"] = data.DEFAULT_BOSS
    kwargs["roles"] = data.ROLES
    kwargs["comps"] = warcraftlogs_comps.CompConfig.objects
    return flask.render_template("index.html", **kwargs)


@blueprint.get("/help")
@cache.cached()
def help():
    """Render the help page."""
    return flask.render_template("help.html")


@blueprint.route("/test")
def test():

    spec = data.SHAMAN_RESTORATION
    boss = data.PAINSMITH

    # Return
    kwargs = {}
    kwargs["data"] = data
    kwargs["spec"] = spec
    kwargs["boss"] = boss
    kwargs["spells"] = spec.spells
    kwargs["bosses"] = boss.zone.bosses
    return flask.render_template("test.html", **kwargs)


################################################################################
#
#   SPEC RANKINGS
#
################################################################################

@blueprint.route("/spec_ranking/<string:spec_slug>/<string:boss_slug>")
@cache.cached()
def spec_ranking(spec_slug, boss_slug):

    spec = WowSpec.get(full_name_slug=spec_slug)
    boss = encounters.RaidBoss.get(name_slug=boss_slug)

    if not spec:
        flask.abort(404, description="Invalid Spec")
    if not boss:
        flask.abort(404, description="Invalid Boss")

    # Return
    kwargs = {}
    kwargs["data"] = data
    kwargs["spec"] = spec
    kwargs["boss"] = boss
    kwargs["spells"] = spec.spells
    kwargs["bosses"] = boss.zone.bosses
    return flask.render_template("spec_ranking.html", **kwargs)


################################################################################
#
#   COMPS
#
################################################################################


@blueprint.route("/comp_ranking/<string:comp_name>/<string:boss_slug>")
@cache.cached(timeout=60)
def comp_ranking(comp_name, boss_slug):
    comp_ranking = warcraftlogs_comps.CompRating.get_or_create(comp=comp_name, boss_slug=boss_slug)

    kwargs = {}
    kwargs["comp_ranking"] = comp_ranking
    kwargs["all_spells"] = comp_ranking.spells_used
    kwargs["timeline_duration"] = max(fight.duration for fight in comp_ranking.fights) if comp_ranking.fights else 0

    kwargs["roles"] = data.ROLES
    kwargs["bosses"] = comp_ranking.boss.zone.bosses

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
        return flask.redirect(flask.url_for("ui.report", report_id=report_id))

    kwargs = {}
    kwargs["form"] = form
    return flask.render_template("report_index.html", **kwargs)


@blueprint.route("/report/<string:report_id>")
async def report(report_id):

    user_report = warcraftlogs_report.UserReport.objects(report__report_id=report_id).first()
    if not user_report:
        flask.abort(404, description="Report not found")

    report = user_report.report

    players = utils.uniqify(report.players, key=lambda player: player.source_id)
    spells_used = utils.flatten(player.spells_used for player in players)
    spells_used = utils.uniqify(spells_used, key=lambda spell: (spell.spell_id, spell.group))

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
