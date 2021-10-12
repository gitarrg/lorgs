"""API-Routes to fetch static Data.

eg.: spells, classes, specs
"""

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
    all_specs = [specs.as_dict(spells=False) for specs in all_specs]
    return {"specs": all_specs}


@blueprint.get("/specs/<string:spec_slug>")
@cache.cached()
def get_spec(spec_slug):
    spec = specs.WowSpec.get(full_name_slug=spec_slug)
    if not spec:
        return "Invalid Spec.", 404
    return spec.as_dict()


@blueprint.get("/specs/<string:spec_slug>/spells")
@cache.cached()
def get_spec_spells(spec_slug):
    """Get all spells for a given spec.

    Args:
        spec_slug (str): name of the spec

    """
    spec = specs.WowSpec.get(full_name_slug=spec_slug)
    if not spec:
        return "Invalid Spec.", 404
    return {spell.spell_id: spell.as_dict() for spell in spec.spells}


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
    """Get all Spells."""
    spells = specs.WowSpell.all
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
    """Get all Bosses for a given Zone.

    Args:
        zone_id (int, optional)

    """
    zone = encounters.RaidZone.get(id=zone_id)
    if not zone:
        return "Invalid Zone.", 404
    return zone.as_dict()


@blueprint.get("/boss/<string:boss_slug>")
@cache.cached(query_string=True)
def get_boss(boss_slug):
    """Get a single Boss.

    Args:
        boss_slug (string): name of the boss

    """
    boss = encounters.RaidBoss.get(full_name_slug=boss_slug)
    if not boss:
        return "Invalid Boss.", 404
    return boss.as_dict()


@blueprint.get("/boss/<string:boss_slug>/spells")
def get_boss_spells(boss_slug):
    """Get Spells for a given Boss.

    Args:
        boss_slug (string): name of the boss

    """
    boss = encounters.RaidBoss.get(full_name_slug=boss_slug)
    if not boss:
        return "Invalid Boss.", 404
    return {spell.spell_id: spell.as_dict() for spell in boss.spells}

