#!/usr/bin/env python
"""Models for Raids and RaidBosses."""

# IMPORT STANDARD LIBRARIES

# IMPORT THIRD PARTY LIBRARIES
import dotenv
dotenv.load_dotenv() # pylint: disable=wrong-import-position

# IMPORT LOCAL LIBRARIES
from lorgs import db
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


def create():
    print("creating encounters")

    for zone_data in _ENCOUNTER_DATA:
        zone = RaidZone(id=zone_data["id"], name=zone_data["name"])

        for i, boss_data in enumerate(zone_data.get("encounters", [])):
            boss = RaidBoss(
                zone_id=zone.id,
                id=boss_data["id"],
                name=boss_data["name"],
                order=i,
            )
            zone.bosses.append(boss)

        db.session.add(zone)


def main():
    with db.session_context(commit=True):
        create()


if __name__ == '__main__':
    main()
