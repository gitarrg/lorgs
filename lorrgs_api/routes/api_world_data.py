"""API-Routes to fetch static Data.

eg.: spells, classes, specs
"""

# IMPORT THIRD PARTY LIBRARIES
import fastapi

# IMPORT LOCAL LIBRARIES
from lorgs.models.raid_boss import RaidBoss
from lorgs.models.raid_zone import RaidZone
from lorgs.models.wow_class import WowClass
from lorgs.models.wow_role import WowRole
from lorgs.models.wow_spec import WowSpec
from lorgs.models.wow_spell import WowSpell

router = fastapi.APIRouter()


###############################################################################
#
#       Roles
#
###############################################################################


@router.get("/roles")
async def get_roles():
    """Get all roles (tank, heal, mpds, rdps)."""
    return {"roles": [role.as_dict() for role in WowRole.list()]}


###############################################################################
#
#       Classes
#
###############################################################################


@router.get("/classes")
async def get_classes():
    return {c.name_slug: c.as_dict() for c in WowClass.list()}


###############################################################################
#
#       Specs
#
###############################################################################


@router.get("/specs", tags=["specs"])
async def get_specs_all():
    all_specs = sorted(WowSpec.list())
    all_specs = [spec.as_dict() for spec in all_specs]  # type: ignore
    return {"specs": all_specs}


@router.get("/specs/{spec_slug}", tags=["specs"])
async def get_spec(spec_slug: str):
    spec = WowSpec.get(full_name_slug=spec_slug)
    if not spec:
        return "Invalid Spec.", 404
    return spec.as_dict()


@router.get("/specs/{spec_slug}/spells", tags=["specs"])
async def get_spec_spells(spec_slug: str):
    """Get all spells for a given spec.

    Args:
        spec_slug (str): name of the spec

    """
    spec: WowSpec = WowSpec.get(full_name_slug=spec_slug)
    if not spec:
        return "Invalid Spec.", 404

    abilities = spec.all_spells + spec.all_buffs + spec.all_debuffs + spec.all_events
    return {spell.spell_id: spell.as_dict() for spell in abilities}


###############################################################################
#
#       Spells
#
###############################################################################


@router.get("/spells/{spell_id}", tags=["spells"])
async def spells_one(spell_id: int):
    """Get a single Spell by spell_id."""
    spell = WowSpell.get(spell_id=spell_id)
    if not spell:
        return "Spell not found", 400
    return spell.as_dict()


@router.get("/spells", tags=["spells"])
async def spells_all():
    """Get all Spells."""
    spells = WowSpell.list()
    return {spell.spell_id: spell.as_dict() for spell in spells}


###############################################################################
#
#       Zones
#
###############################################################################


@router.get("/zones", tags=["raids"])
async def get_zones():
    """Get all raid-zones."""
    zones = RaidZone.list()
    return [zone.as_dict() for zone in zones]


@router.get("/zones/{zone_id}", tags=["raids"])
async def get_zone(zone_id: int):
    """Get a specific (raid-)Zone."""
    zone = RaidZone.get(id=zone_id)
    if not zone:
        return "Invalid Zone.", 404
    return zone.as_dict()


@router.get("/zones/{zone_id}/bosses", tags=["raids"])
async def get_zone_bosses(zone_id: int):
    """Get all Bosses in a given Raid Zone."""
    zone = RaidZone.get(id=zone_id)
    if not zone:
        return "Invalid Zone.", 404
    return {boss.name_slug: boss.as_dict() for boss in zone.bosses}


###############################################################################
#
#       Bosses
#
###############################################################################


@router.get("/bosses", tags=["raids"])
async def get_bosses():
    """Gets all Bosses
    Warning:
        this does not filter by raid.
        use "/zone/<zone_id>/bosses" to only get the bosses for a given raid.
    """
    return {"bosses": [boss.as_dict() for boss in RaidBoss.list()]}


@router.get("/bosses/{boss_slug}", tags=["raids"])
async def get_boss(boss_slug: str):
    """Get a single Boss.

    Args:
        boss_slug (string): name of the boss

    """
    boss = RaidBoss.get(full_name_slug=boss_slug)
    if not boss:
        return "Invalid Boss.", 404
    return boss.as_dict()


@router.get("/bosses/{boss_slug}/spells", tags=["raids"])
async def get_boss_spells(boss_slug: str):
    """Get Spells for a given Boss.

    Args:
        boss_slug (string): name of the boss

    """
    boss = RaidBoss.get(full_name_slug=boss_slug)
    if not boss:
        return "Invalid Boss.", 404

    spells = boss.all_spells + boss.all_buffs + boss.all_debuffs + boss.all_events
    return {spell.spell_id: spell.as_dict() for spell in spells}
