"""Views/Routes for the UI/Frontend."""

# IMPORT THIRD PARTY LIBS
import re
import flask

# IMPORT LOCAL LIBS
from lorgs import utils
from lorgs import data
from lorgs import forms
from lorgs import models
from lorgs.cache import Cache


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




@BP.app_context_processor
def add_shared_variables():
    config = flask.current_app.config
    return {
        # "wow_data": wow_data,
        "GOOGLE_ANALYTICS_ID": config["GOOGLE_ANALYTICS_ID"],

        "spec_ranking_color": spec_ranking_color,
    }


@BP.route("/", methods=['GET', 'POST'])
def index():
    """Main Route for the index page."""
    form = forms.CustomReportForm()

    if form.validate_on_submit():
        link = form.report_link.data
        match = re.match(forms.WCL_LINK_REGEX, link)
        report_id = match.group("code")

        flask.flash(f"valid link: {report_id}")
        return flask.redirect(flask.url_for("ui.report", report_id=report_id))

    kwargs = {}
    kwargs["form"] = form
    kwargs["boss"] = data.DEFAULT_BOSS
    kwargs["roles"] = data.ROLES
    return flask.render_template("index.html", **kwargs)


@BP.route("/spec_ranking/<spec_slug>_<boss_slug>")
def spec_ranking(spec_slug, boss_slug):

    # Inputs
    spec = models.WowSpec.get(full_name_slug=spec_slug)
    boss = models.RaidBoss.get(name_slug=boss_slug)
    if not (spec and boss):
        # TODO: add proper error message
        return {
            "boss": {"slug:": boss_slug, "str": str(boss)},
            "spec": {"slug:": spec_slug, "str": str(spec)},
        }

    # Get Data
    key = f"char_rankings/{spec.full_name_slug}/boss={boss.name_slug}"
    players = Cache.get(key) or []
    """
    # for now.. I don't want this to trigger on its own
    if not players:
        players = asyncio.run(loader.load_char_rankings(boss, spec, limit=5))
        Cache.set(key, players)
    """

    # used_spells = [cast.spell for player in players for cast in player.casts]
    used_spells = utils.uniqify(spec.spells, key=lambda spell: spell.spell_id)

    # Return
    kwargs = {}
    kwargs["spec"] = spec
    kwargs["boss"] = boss
    kwargs["players"] = players
    kwargs["all_spells"] = used_spells
    kwargs["timeline_duration"] = max(player.fight.duration for player in players) if players else 0

    # Data for Nav
    kwargs["roles"] = data.ROLES
    kwargs["bosses"] = data.BOSSES # TODO: current zone only
    return flask.render_template("spec_ranking.html", **kwargs)


@BP.route("/report/<string:report_id>")
def report(report_id):

    report = Cache.get(f"report/{report_id}")
    if not report:
        return {"error": "report not found"}

    # report.fights = report.fights[:3]

    specs = [player.spec for player in report.players]
    specs = utils.uniqify(specs, key=lambda spec: spec.full_name)
    used_spells = utils.flatten([spec.spells for spec in specs])
    used_spells = utils.uniqify(used_spells, key=lambda spell: (spell.group, spell.spell_id))

    kwargs = {

        "report": report,
        "all_spells": used_spells,
        "timeline_duration": max(f.duration for f in report.fights),

        # Data for Nav
        "roles": data.ROLES,
        "bosses": data.BOSSES # TODO: current zone only
    }
    return flask.render_template("report.html", **kwargs)
