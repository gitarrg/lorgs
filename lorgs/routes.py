"""Views/Routes for the UI/Frontend."""

# IMPORT THIRD PARTY LIBS
import os
import re
# import arrow
import flask

import sqlalchemy

# IMPORT LOCAL LIBS
from lorgs import models
from lorgs import utils
from lorgs.logger import logger
# from lorgs import wow_data
from lorgs.db import db
from lorgs.models import loader
from lorgs import forms

# some hacked config
DEFAULT_ENCOUNTER = 2407 # Sire Denathrius


BP = flask.Blueprint(
    "ui",
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="/"
)



@BP.context_processor
def add_shared_variables():

    config = flask.current_app.config

    return {
        # "wow_data": wow_data,
        "GOOGLE_ANALYTICS_ID": config["GOOGLE_ANALYTICS_ID"],
    }

def _get_spec_by_slug(slug):
    for spec in models.WowSpec.query.all():
        if spec.full_name_slug == slug:
            return spec

def _get_boss_by_slug(slug):
    print("_get_boss_by_slug", slug)
    for boss in models.RaidBoss.query.all():
        print("_get_boss_by_slug", slug, boss.name_slug)
        if boss.name_slug == slug:
            return boss


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

    # we need smth to make the links work
    kwargs["boss"] = models.RaidBoss.query.first()

    kwargs["roles"] = models.WowRole.query\
        .options(sqlalchemy.orm.joinedload("specs"))\
        .options(sqlalchemy.orm.joinedload("specs.wow_class"))\
        .all()

    return flask.render_template("index.html", **kwargs)


@BP.route("/spell_db")
def spell_db():
    spells = models.WowSpell.query.all()
    return flask.render_template("elements/spell_db.js", spells=spells)


@BP.route("/spec_ranking/<spec_slug>_<boss_slug>")
def spec_ranking(spec_slug, boss_slug):

    spec = _get_spec_by_slug(spec_slug)
    boss = _get_boss_by_slug(boss_slug)
    if not (spec and boss):
        return flask.jsonify(
            {
                "boss": {"slug:": boss_slug, "str": str(boss)},
                "spec": {"slug:": spec_slug, "str": str(spec)},
            }
        )

    players = models.Player.query

    # Filter by Spec
    players = players.filter(models.Player.spec == spec)

    # Filter by Boss
    players = players.join(models.Player.fight)
    players = players.join(models.Fight.boss)
    players = players.filter(models.Fight.boss == boss)

    # Order/Limit/run
    players = players.order_by(models.Player.total.desc())
    # players = players.limit(50)
    players = players.all()

    # longest_fight = sorted(fights, key=lambda f: f.duration)[-1]

    kwargs = {
        "spec": spec,
        "boss": boss,
        "players": players,

        "all_spells": spec.spells,

        "timeline_duration": 2000,

        # Data for Nav
        "roles": models.WowRole.query.all(),
        "bosses": models.RaidBoss.query.all(), # TODO: current zone only?
    }
    return flask.render_template("spec_ranking.html", **kwargs)


@BP.route("/report/<string:report_id>")
def report(report_id):

    report = models.Report.query \
        .filter_by(report_id=report_id) \
        .options(sqlalchemy.orm.joinedload("fights")) \
        .options(sqlalchemy.orm.joinedload("fights.players")) \
        .options(sqlalchemy.orm.joinedload("fights.players.casts")) \
        .options(sqlalchemy.orm.joinedload("fights.players.spec")) \
        .options(sqlalchemy.orm.joinedload("fights.players.spec.wow_class")) \
        .first()

    if not report:
        report = models.Report(report_id=report_id)
        import asyncio
        report = asyncio.run(loader.load_report(report))
        db.session.add(report)
        db.session.commit()

    durations = [f.duration for f in report.fights]

    kwargs = {

        "report": report,

        # "spec": spec,
        # "boss": boss,
        # "players": players,

        "all_spells": report.used_spells,

        "timeline_duration": max(durations),

        # Data for Nav
        "roles": models.WowRole.query.all(),
        "bosses": models.RaidBoss.query.all(), # TODO: current zone only?
    }
    return flask.render_template("report.html", **kwargs)
