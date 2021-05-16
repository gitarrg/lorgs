"""Views/Routes for the UI/Frontend."""

# IMPORT THIRD PARTY LIBS
import flask

# IMPORT LOCAL LIBS
# from lorgs import db
# from lorgs import forms
# from lorgs.logger import logger
# from lorgs import models
# from lorgs import tasks
from lorgs import data
from lorgs import utils
# from lorgs.cache import Cache
from lorgs.models import encounters
# from lorgs.models import specs
# from lorgs.models import warcraftlogs
from lorgs.models import warcraftlogs_ranking
from lorgs.models import warcraftlogs_comps
# from lorgs.models import warcraftlogs_report


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


################################################################################
#
#   GLOBAL
#
################################################################################


@BP.route("/")
def index():
    """Render the main index page."""
    kwargs = {}
    kwargs["boss"] = encounters.RaidBoss.get(id=DEFAULT_BOSS_ID)
    kwargs["roles"] = data.ROLES

    kwargs["comps"] = warcraftlogs_comps.CompConfig.objects

    return flask.render_template("index.html", **kwargs)


################################################################################
#
#   SPEC RANKINGS
#
################################################################################

@BP.route("/spec_ranking/<string:spec_slug>/<string:boss_slug>")
def spec_ranking(spec_slug, boss_slug):

    # Inputs
    # limit = flask.request.args.get("limit", default=50, type=int)
    spec_ranking = warcraftlogs_ranking.SpecRanking.objects(boss_slug=boss_slug, spec_slug=spec_slug).first()
    if not spec_ranking:
        flask.abort(404, description="Invalid Spec or Boss")

    # preprocess some data
    spells_used = utils.flatten(player.spells_used for player in spec_ranking.players)
    spells_used = utils.uniqify(spells_used, key=lambda spell: spell)
    timeline_duration = max(fight.duration for fight in spec_ranking.fights) if spec_ranking.fights else 0

    # Return
    kwargs = {}
    kwargs["spec"] = spec_ranking.spec
    kwargs["boss"] = spec_ranking.boss
    kwargs["players"] = spec_ranking.players
    kwargs["all_spells"] = spells_used
    kwargs["timeline_duration"] = timeline_duration

    kwargs["roles"] = data.ROLES
    kwargs["bosses"] = data.CASTLE_NATHRIA.bosses # encounters.RaidBoss.all

    return flask.render_template("spec_ranking.html", **kwargs)

################################################################################
#
#   COMPS
#
################################################################################


@BP.route("/comp_ranking/<string:comp_name>/<string:boss_slug>")
def comp_ranking(comp_name, boss_slug):
    comp_ranking = warcraftlogs_comps.CompRating.get_or_create(comp=comp_name, boss_slug=boss_slug)

    kwargs = {}
    kwargs["comp"] = comp_ranking.comp
    kwargs["boss"] = comp_ranking.boss
    kwargs["reports"] = comp_ranking.reports

    kwargs["all_spells"] = comp_ranking.spells_used
    kwargs["timeline_duration"] = 0

    kwargs["roles"] = data.ROLES
    kwargs["bosses"] = data.CASTLE_NATHRIA.bosses

    return flask.render_template("comp_ranking.html", **kwargs)


################################################################################
#
#   REPORTS
#
################################################################################

'''
@BP.route("/report", methods=['GET', 'POST'])
@BP.route("/reports", methods=['GET', 'POST'])
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

    # query them all into memory
    all_spells = specs.WowSpell.query.all()

    report = warcraftlogs_report.Report.query
    report = report.options(
        sa.orm.joinedload("fights"),
        sa.orm.joinedload("fights.boss"),
        sa.orm.joinedload("fights.players"),
        sa.orm.joinedload("fights.players.spec"),
    )
    report = report.get(report_id)

    if not report:
        flask.abort(404, description="Report not found")
        # return flask.redirect(flask.url_for("ui.report_load", report_id=report_id))

    players = utils.uniqify(report.players, key=lambda player: player.source_id)
    used_spells = utils.flatten(player.used_spells for player in players)
    used_spells = utils.uniqify(used_spells, key=lambda spell: (spell.spell_id, spell.group))

    kwargs = {
        "report": report,

        "unique_players": players,
        "all_spells": used_spells,
        "timeline_duration": max(f.duration for f in report.fights) if report.fights else 0,
    }
    return flask.render_template("report.html", **kwargs)
'''