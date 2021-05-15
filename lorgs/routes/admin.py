"""Views/Routes for some debugging/admin stuff."""

# IMPORT THIRD PARTY LIBS
import flask

# IMPORT LOCAL LIBS
from lorgs import db
# from lorgs import forms
# from lorgs import models
# from lorgs import tasks
# from lorgs import utils
from lorgs import data
# from lorgs.cache import Cache
from lorgs.models import encounters
from lorgs.models import specs
# from lorgs.models import warcraftlogs
from lorgs.models import warcraftlogs_ranking


BP = flask.Blueprint(
    "admin",
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="/"
)

SHARED_DATA = {}


@BP.route("/")
def index():
    flask.abort(401, description="sorry.. no admin page for you")


@BP.route("/spells")
def spells():
    kwargs = {}
    kwargs["specs"] = data.SPECS
    # kwargs["spells"] = specs.SpecSpells.query.all()
    return flask.render_template("admin/admin_spells.html", **kwargs)


@BP.route("/spec_rankings")
def spec_rankings():


    ranked_chars = (
        db.session.query(
            warcraftlogs_ranking.RankedCharacter.spec_id,
            warcraftlogs_ranking.RankedCharacter.boss_id,
            sa.sql.func.count(warcraftlogs_ranking.RankedCharacter.uuid),
        )
        .group_by(
            warcraftlogs_ranking.RankedCharacter.spec_id,
            warcraftlogs_ranking.RankedCharacter.boss_id,
        )
        .all()
    )


    kwargs = {}
    kwargs["specs"] = specs.WowSpec.query.filter(specs.WowSpec.id < 1000).all()
    kwargs["bosses"] = encounters.RaidBoss.query.all()
    kwargs["spec_rankings"] = {(s, b): c for s, b, c in ranked_chars}

    return flask.render_template("admin/admin_spec_rankings.html", **kwargs)
