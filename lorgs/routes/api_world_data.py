"""API-Routes to fetch static Data.

eg.: spells, classes, specs
"""

# IMPORT STANDARD LIBRARIES
import json

# IMPORT THIRD PARTY LIBRARIES
import flask

# IMPORT LOCAL LIBRARIES
from lorgs.cache import cache
from lorgs.models import encounters, specs


blueprint = flask.Blueprint("api.world_data", __name__)


###############################################################################
#
#       Roles
#
###############################################################################

@blueprint.get("/roles")
@cache.cached()
def get_roles():
    """Get all roles (tank, heal, mpds, rdps)."""
    return {
        "roles": [role.as_dict() for role in specs.WowRole.all]
    }


###############################################################################
#
#       Specs
#
###############################################################################

@blueprint.get("/specs")
@cache.cached(query_string=True)
def get_specs_all():
    all_specs = sorted(specs.WowSpec.all)
    all_specs = [specs.as_dict(spells=True) for specs in all_specs]
    return {"specs": all_specs}


@blueprint.get("/specs/<string:spec_slug>")
@cache.cached()
def get_spec(spec_slug):
    spec = specs.WowSpec.get(full_name_slug=spec_slug)
    if not spec:
        return "Invalid Spec.", 404
    return spec.as_dict()



###############################################################################
#
#       Spells
#
###############################################################################

@blueprint.get("/spells/<int:spell_id>")
@cache.cached()
def spells_one(spell_id):
    """Get a single Spell by spell_id."""
    spell = specs.WowSpell.get(spell_id=spell_id)
    if not spell:
        flask.abort(404, description="Spell not found")
    return spell.as_dict()


@blueprint.get("/spells")
@cache.cached()
def spells_all():

    spells = specs.WowSpell.all

    # filter by group
    # groups = flask.request.args.getlist("group") #, default="", type=str)
    # if groups:
    #     # TODO: change this to use `spell.specs` or some other method
    #     spells = [spell for spell in spells if spell.group and spell.group.full_name_slug in groups]

    return {spell.spell_id: spell.as_dict() for spell in spells}


###############################################################################
#
#       Bosses
#
###############################################################################

@blueprint.get("/bosses")
@blueprint.get("/zone/bosses")
@blueprint.get("/zone/<int:zone_id>/bosses")
@cache.cached()
def get_bosses(zone_id=28):
    zone = encounters.RaidZone.get(id=zone_id)
    if not zone:
        return "Invalid Zone.", 404
    return zone.as_dict()


@blueprint.get("/boss/<string:boss_slug>")
@cache.cached(query_string=True)
def get_boss(boss_slug):
    include_spells = flask.request.args.get("include_spells", default=True, type=json.loads)
    boss = encounters.RaidBoss.get(full_name_slug=boss_slug)
    if not boss:
        return "Invalid Boss.", 404
    return boss.as_dict(include_spells=include_spells)
