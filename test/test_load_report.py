# pylint: disable=wrong-import-position,invalid-name

# IMPORT STANDARD LIBRARIES
import os
import pprint
import asyncio

# IMPORT THIRD PARTY LIBRARIES
import dotenv
dotenv.load_dotenv()
os.environ["DEBUG"] = "1"

# from lorgs.app import create_app
# from lorgs.cache import Cache
# from lorgs import db
from lorgs import data
from lorgs import utils
# from lorgs.client import WarcraftlogsClient
# from lorgs.models import loader
# from lorgs.models import RaidBoss
# from lorgs.models import WowClass
from lorgs.models import specs
from lorgs.models import WowSpec
# from lorgs.models.warcraftlogs_report import Report
from lorgs.models import warcraftlogs_report
from lorgs.models import warcraftlogs_actor


# create app instance
# app = create_app()
# app.app_context().push()

# db.Base.metadata.create_all(db.engine)

report_id = "yNmZQ3rknCBt8KTz"


async def test_load_report():
    # report_id = "yHQTNpvtkVjw82ca" # AM Sunday

    user_report = warcraftlogs_report.UserReport.get_or_create(report_id=report_id)

    if user_report.report:
        user_report.report.fights = []

    await user_report.load(fight_ids=[8])
    report = user_report.report
    user_report.save()

    for fight in report.fights:

        for player in fight.players:
            print(2, player, len(player.casts))
            print(2, player, len(player.deaths))



        """
        casts = utils.uniqify(fight.boss.casts, lambda cast: (cast.spell_id, cast.timestamp))
        for cast in casts:
            print(cast, cast.spell.name)
        return
        """

        # casts = utils.uni


        print("fight.boss", fight.boss)
        for cast in fight.boss.casts:
            print(cast, cast.spell.name)

        # await fight.boss.load()
        # await fight.load_many(fight.players + [fight.boss])
        """
        for player in fight.players:
            print(player)
        """
    return

    """
        print(fight)
        print(fight.boss)

        print("##########")
        print(fight.boss.get_query())
        print("##########")
        # print(fight.boss.raid_boss.name)


        # for player in fight.players:
    """

    """
    report = warcraftlogs_base.Report(report_id=report_id)
    await report.load(fight_ids=[7, 8, 9, 10])
    """

    """
    for fight in report.fights:
        print(fight)

        for player in fight.players:
            print("\t", player, len(player.casts))
    """

    # return
    # await report.load_report_info(fight_ids=[7, 8, 9, 10])

    """
    for fight in report.fights:
        print(fight)
        print(fight.raid_boss)
        await fight.load_boss_events()

        for cast in fight.boss.casts:
            print(cast)
    """

    # user_report.report = report
    user_report.save()

    return


    # fight = report.add_fight()
    # fight.fight_id = 10
    # fight.boss_id = 2399
    # fight.boss = warcraftlogs_base.Boss(boss_id=2399)

    # print(fight.raid_boss)

    boss = fight.boss

    # print(repr(fight))
    # print(repr(fight.boss))
    # print(repr(fight.boss.boss))

    # await fight.load_boss_events()

    # print(boss, boss.boss)


    return

    await report.load()

    print(report)

    for fight in report.fights:
        print(repr(fight), fight.boss.name)
    return


def get_report():

    user_report = warcraftlogs_base.UserReport.objects(report__report_id=report_id).first()
    print(user_report)
    print(user_report.id)

    report = user_report.report
    for fight in report.fights:
        print(fight.boss)

    return

    for fight in report.fights:

        if fight.fight_id != 19:
            continue

        for player in fight.players:

            if player.source_id != 20:
                continue

            # print(player.casts)
            # print(player.spec.spells)
            # print(player.used_spells)
            print(player.death_data)
            print(player.lifetime, utils.format_time(player.lifetime))
            print(player.fight.duration, utils.format_time(player.fight.duration))
            # print(player.fight.start_time, utils.format_time(player.fight.start_time))


            return


async def main():
    await test_load_report()
    # get_report()





if __name__ == '__main__':
    asyncio.run(main())
