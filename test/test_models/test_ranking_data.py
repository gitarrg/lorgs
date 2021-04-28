# pylint: disable=wrong-import-position,invalid-name

# IMPORT STANDARD LIBRARIES
import asyncio
import pprint

# IMPORT THIRD PARTY LIBRARIES
import dotenv
import sqlalchemy
dotenv.load_dotenv()

from lorgs.app import create_app
from lorgs.client import WarcraftlogsClient
from lorgs.db import db

from lorgs.models.specs import WowClass, WowSpec
from lorgs.models.encounters import RaidBoss
from lorgs.models.reports import Report, Fight, Player, Cast


# create app instance

WCL_CLIENT = WarcraftlogsClient.get_instance()

async def test1_load():
    spec = WowSpec.query.join(WowSpec.wow_class) # join the class so we can filter
    spec = spec.filter(WowClass.name == "Paladin")
    spec = spec.filter(WowSpec.name == "Holy")
    spec = spec.first()

    print("test1_load", 1)
    boss = RaidBoss.query.filter_by(name="Sludgefist").first()

    print("test1_load", 2)
    reports = await WCL_CLIENT.get_rankings(boss, spec)
    # reports = reports[:5]

    print("test1_load", 3)
    for report in reports:
        print(report)
        for fight in report.fights:
            print("\t", fight)
            for player in fight.players:
                print("\t\t", player.fight, player)

    db.session.bulk_save_objects(reports)
    db.session.commit()


async def test2_load_casts():

    spec = WowSpec.query.join(WowSpec.wow_class) # join the class so we can filter
    spec = spec.filter(WowClass.name == "Paladin")
    spec = spec.filter(WowSpec.name == "Holy")
    spec = spec.first()

    boss = RaidBoss.query.filter_by(name="Sludgefist").first()

    players = Player.query
    players = players.filter_by(spec=spec)
    players = players.order_by(Player.total.desc())
    players = players.limit(3)
    players.all()

    queries = [p.get_casts_query() for p in players]
    data = await WCL_CLIENT.multiquery(queries)

    for player, cast_data in zip(players, data):

        player.process_cast_data(cast_data)
        print("######################")
        print("Player", player)
        for cast in player.casts:
            print("Cast", cast.id, cast.player.id, cast)

    db.session.bulk_save_objects(players)
    db.session.commit()

    # pprint.pprint(data)
    return



async def test2_read():


    report = Report.query.first()
    print("R", report)
    print("F", report.fights)
    print("P", report.players)

    spec = WowSpec.query.join(WowSpec.wow_class) # join the class so we can filter
    spec = spec.filter(WowClass.name == "Paladin")
    spec = spec.filter(WowSpec.name == "Holy")
    spec = spec.first()
    boss = RaidBoss.query.filter_by(name="Sludgefist").first()

    players = Player.query
    players = players.filter_by(spec=spec)
    players = players.order_by(Player.total.desc())

    # players = players.join(Player.casts)
    # players = players.having(sqlalchemy.func.count(Cast.id) > 0)

    players = players.limit(10)
    players.all()

    for player in players:
        print(f"{player.total:,} | {player.name} | {len(player.casts)}")
        """
        print(player)
        for cast in player.casts:
            print("Cast", cast)
        """
    return
    return


async def main():
    await WCL_CLIENT.cache.load()
    app = create_app()
    app.app_context().push()

    # await test1_load()
    await test2_load_casts()
    # await test2_read()

    await WCL_CLIENT.cache.save()



if __name__ == '__main__':
    asyncio.run(main())

