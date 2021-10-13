"""Views/Routes for some debugging/admin stuff."""

# IMPORT THIRD PARTY LIBS
import flask

# IMPORT LOCAL LIBS
from lorgs import data
from lorgs import utils
from lorgs.cache import cache
from lorgs.models import warcraftlogs_ranking
from lorgs.models.specs import WowSpec


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


# @cache.cached(timeout=600)
@blueprint.get("/spells/")
@blueprint.get("/spellbook/")
@blueprint.get("/spells/<group_name>")
@blueprint.get("/spellbook/<group_name>")
def spells(group_name=None):

    kwargs = {}

    spells = data.ALL_SPELLS

    if group_name:
        group = WowSpec.get(full_name_slug=group_name)
        if group:
            kwargs["group"] = group
            spells = [spell for spell in spells if group in (spell.group, spell.spec)]
    spells = utils.uniqify(spells, key=lambda spell: spell.spell_id)

    kwargs["specs"] = WowSpec.all
    kwargs["spells"] = spells

    return flask.render_template("admin/admin_spells.html", **kwargs)


@blueprint.get("/spec_rankings")
@cache.cached(timeout=60)
def spec_rankings():


    bosses = data.SANCTUM_OF_DOMINATION_BOSSES
    roles = data.ROLES
    specs = utils.flatten(role.specs for role in roles)

    spec_rankings_data = {}
    for spec_ranking in warcraftlogs_ranking.SpecRanking.objects().exclude("reports").all():
        spec_rankings_data.setdefault(spec_ranking.spec_slug, {})
        spec_rankings_data[spec_ranking.spec_slug][spec_ranking.boss_slug] = spec_ranking

    for spec in specs:
        spec_rankings_data.setdefault(spec.full_name_slug, {})
        for boss in bosses:
            spec_rankings_data[spec.full_name_slug].setdefault(boss.full_name_slug, None)

    kwargs = {}
    kwargs["bosses"] = bosses
    kwargs["roles"] = roles
    kwargs["specs"] = specs
    kwargs["spec_ranking_data"] = spec_rankings_data


    return flask.render_template("admin/admin_spec_rankings.html", **kwargs)


@blueprint.get("/updater")
@cache.cached(timeout=60)
def updater():

    bosses = data.SANCTUM_OF_DOMINATION_BOSSES
    roles = data.ROLES
    specs = utils.flatten(role.specs for role in roles)

    kwargs = {}
    kwargs["bosses"] = bosses
    kwargs["roles"] = roles
    kwargs["specs"] = specs
    return flask.render_template("admin/admin_spec_updater.html", **kwargs)
