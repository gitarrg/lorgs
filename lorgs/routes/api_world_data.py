"""API-Routes to fetch static Data.

eg.: spells, classes, specs
"""

# IMPORT THIRD PARTY LIBRARIES
import quart

# IMPORT LOCAL LIBRARIES
from lorgs.cache import cache
from lorgs.models.raid_boss import RaidBoss
from lorgs.models.raid_zone import RaidZone
from lorgs.models.wow_role import WowRole
from lorgs.models.wow_spec import WowSpec
from lorgs.models.wow_spell import WowSpell


blueprint = quart.Blueprint("api/world_data", __name__)


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
        "roles": [role.as_dict() for role in WowRole.all]
    }


###############################################################################
#
#       Specs
#
###############################################################################

@blueprint.get("/specs")
@cache.cached(query_string=True)
def get_specs_all():
    all_specs = sorted(WowSpec.all)
    all_specs = [specs.as_dict() for specs in all_specs]
    return {"specs": all_specs}


@blueprint.get("/specs/<string:spec_slug>")
@cache.cached()
def get_spec(spec_slug):
    spec = WowSpec.get(full_name_slug=spec_slug)
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
    spec: WowSpec = WowSpec.get(full_name_slug=spec_slug)
    if not spec:
        return "Invalid Spec.", 404

    abilities = spec.all_spells + spec.all_buffs
    return {spell.spell_id: spell.as_dict() for spell in abilities}


###############################################################################
#
#       Spells
#
###############################################################################

@blueprint.get("/spells/<int:spell_id>")
@cache.cached()
def spells_one(spell_id):
    """Get a single Spell by spell_id."""
    spell = WowSpell.get(spell_id=spell_id)
    if not spell:
        quart.abort(404, description="Spell not found")
    return spell.as_dict()


@blueprint.get("/spells")
@cache.cached()
def spells_all():
    """Get all Spells."""
    spells = WowSpell.all
    return {spell.spell_id: spell.as_dict() for spell in spells}


###############################################################################
#
#       Zones
#
###############################################################################

@blueprint.get("/zones")
@cache.cached()
def get_zones():
    """Get all raid-zones."""
    zones = RaidZone.all
    return {zone.id: zone.as_dict() for zone in zones}


@blueprint.get("/zones/<int:zone_id>")
@cache.cached()
def get_zone(zone_id):
    """Get a specific (raid-)Zone."""
    zone = RaidZone.get(id=zone_id)
    if not zone:
        return "Invalid Zone.", 404
    return zone.as_dict()


@blueprint.get("/zones/<int:zone_id>/bosses")
@cache.cached()
def get_zone_bosses(zone_id):
    """Get all Bosses in a given Raid Zone."""
    zone = RaidZone.get(id=zone_id)
    if not zone:
        return "Invalid Zone.", 404
    return {boss.full_name_slug: boss.as_dict() for boss in zone.bosses}


###############################################################################
#
#       Bosses
#
###############################################################################



@blueprint.get("/bosses")
@cache.cached()
def get_bosses():
    """Gets all Bosses

    Warning:
        this does not filter by raid.
        use "/zone/<zone_id>/bosses" to only get the bosses for a given raid.

    """
    return {
        "bosses": [boss.as_dict() for boss in RaidBoss.all]
    }


@blueprint.get("/bosses/<string:boss_slug>")
@cache.cached(query_string=True)
def get_boss(boss_slug):
    """Get a single Boss.

    Args:
        boss_slug (string): name of the boss

    """
    boss = RaidBoss.get(full_name_slug=boss_slug)
    if not boss:
        return "Invalid Boss.", 404
    return boss.as_dict()


@blueprint.get("/bosses/<string:boss_slug>/spells")
def get_boss_spells(boss_slug):
    """Get Spells for a given Boss.

    Args:
        boss_slug (string): name of the boss

    """
    boss = RaidBoss.get(full_name_slug=boss_slug)
    if not boss:
        return "Invalid Boss.", 404
    return {spell.spell_id: spell.as_dict() for spell in boss.spells}
