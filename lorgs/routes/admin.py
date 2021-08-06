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
from lorgs import utils
# from lorgs.cache import Cache
from lorgs.models import encounters
from lorgs.models import specs
# from lorgs.models import warcraftlogs
from lorgs.models import warcraftlogs_ranking


blueprint = flask.Blueprint(
    "admin",
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="/"
)

SHARED_DATA = {}


@blueprint.get("/")
def index():
    flask.abort(401, description="sorry.. no admin page for you")


@blueprint.get("/spells")
def spells():
    kwargs = {}
    kwargs["specs"] = data.SPECS
    return flask.render_template("admin/admin_spells.html", **kwargs)


@blueprint.get("/spec_rankings")
def spec_rankings():


    bosses = data.SANCTUM_OF_DOMINATION_BOSSES
    roles = data.ROLES
    specs = utils.flatten(role.specs for role in roles)
    specs = [spec for spec in specs if spec.supported]


    spec_rankings_data = {}
    for spec_ranking in warcraftlogs_ranking.SpecRanking.objects().exclude("reports").all():
        spec_rankings_data.setdefault(spec_ranking.spec_slug, {})
        spec_rankings_data[spec_ranking.spec_slug][spec_ranking.boss_slug] = spec_ranking

    for spec in specs:
        for boss in bosses:
            spec_rankings_data[spec.full_name_slug].setdefault(boss.name_slug, None)



    kwargs = {}
    kwargs["bosses"] = bosses
    kwargs["roles"] = roles
    kwargs["specs"] = specs
    kwargs["spec_ranking_data"] = spec_rankings_data


    return flask.render_template("admin/admin_spec_rankings.html", **kwargs)
