
from lorgs.db import db
from lorgs.models.encounters import RaidZone, RaidBoss


# TODO: get from query?
ENCOUNTER_DATA = [
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
    for zone in ENCOUNTER_DATA:
        raid_zone = RaidZone.get(id=zone["id"], name=zone["name"])
        print(raid_zone.id, raid_zone.name)

        for boss in zone.get("encounters", []):
            raid_boss = RaidBoss.get(zone=raid_zone, boss_id=boss["id"], name=boss["name"])
            print("\t", raid_boss.boss_id, raid_boss.name)

        db.session.add(raid_zone)



if __name__ == '__main__':

    from lorgs.app import create_app

    app = create_app()
    app.app_context().push()
    create()
