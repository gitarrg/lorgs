"""Models for Raids and RaidBosses."""

# IMPORT LOCAL LIBRARIES
from lorgs.models.encounters import RaidZone, RaidBoss


# TODO: get from query?
_ENCOUNTER_DATA = [
    {
        "id": 26,
        "name": "Castle Nathria",
        "encounters": [
            {"id": 2398, "name": "Shriekwing"},
            {"id": 2418, "name": "Huntsman Altimor"},
            {"id": 2383, "name": "Hungering Destroyer"},
            {"id": 2402, "name": "Sun King's Salvation"},
            {"id": 2405, "name": "Artificer Xy'mox"},
            {"id": 2406, "name": "Lady Inerva Darkvein"},
            {"id": 2412, "name": "The Council of Blood"},
            {"id": 2399, "name": "Sludgefist"},
            {"id": 2417, "name": "Stone Legion Generals"},
            {"id": 2407, "name": "Sire Denathrius"},
        ]
    },
]


for zone_data in _ENCOUNTER_DATA:
    zone = RaidZone(id=zone_data["id"], name=zone_data["name"])

    for boss_data in zone_data.get("encounters", []):
        zone.add_boss(id=boss_data["id"], name=boss_data["name"])


DEFAULT_ZONE = RaidZone.get(id=26)
DEFAULT_BOSS = RaidBoss.get(id=2407)

ZONES = RaidZone.all
BOSSES = DEFAULT_ZONE.bosses
