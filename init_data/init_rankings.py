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
from lorgs.logger import logger
from lorgs import utils

from lorgs.models.specs import WowClass, WowSpec
from lorgs.models.encounters import RaidBoss
from lorgs.models.reports import Report, Fight, Player, Cast


WCL_CLIENT = WarcraftlogsClient.get_instance()


LIMIT_PER_BOSS = 10


async def generate_char_rankings(spec, boss):
    logger.info(f"{spec.full_name} vs. {boss.name} START")


    reports = await WCL_CLIENT.get_rankings(boss, spec, limit=LIMIT_PER_BOSS)
    """
    for report in reports:
        print(report)
        for fight in report.fights:
            print("\t", fight)
            for player in fight.players:
                print("\t\t", player.fight, player)
    """

    players = []
    for report in reports:
        for fight in report.fights:
            if fight.boss == boss:
                players += fight.players

    # players = utils.flatten([r.players for r in reports])
    # players = utils.flatten(players)

    queries = [p.get_casts_query() for p in players]
    data = await WCL_CLIENT.multiquery(queries)

    for player, cast_data in zip(players, data):
        player.process_cast_data(cast_data)

    # return
    # print("FIGHTS")
    for player in players:
        print(player.fight.boss.name, player.fight.report.report_id, player.name)


    db.session.bulk_save_objects(reports)
    db.session.commit()

    logger.info(f"{spec.full_name} vs. {boss.name} DONE")
    return


async def main():

    app = create_app()
    app.app_context().push()

    await WCL_CLIENT.cache.load()

    specs = WowSpec.query.all()
    # spec = WowSpec.query
    # spec = spec.filter(WowClass.name == "Paladin")
    # spec = spec.filter(WowSpec.name == "Holy")
    # spec = spec.first()
    # specs = [spec]

    bosses = RaidBoss.query.limit(3).all()

    for spec in specs:

        tasks = [generate_char_rankings(spec, boss) for boss in bosses]
        await asyncio.gather(*tasks)
        """
        for boss in bosses:
            await generate_char_rankings(spec, boss)
            # return
        """

    await WCL_CLIENT.cache.save()


if __name__ == '__main__':
    asyncio.run(main())

