
import asyncio
import pprint
import time

import dotenv
dotenv.load_dotenv() # pylint: disable=wrong-import-position
import mongoengine as me

from lorgs import db
# from lorgs import data
# from lorgs import utils
# from lorgs.app import create_app
# from lorgs.cache import Cache
# from lorgs.models.encounters import RaidBoss
# from lorgs.models.specs import WowSpec
# from lorgs.models.specs import WowSpell
# from lorgs.models import loader
from lorgs.client import WarcraftlogsClient
# from lorgs import tasks

from lorgs.models import warcraftlogs_report
from lorgs.models.warcraftlogs_fight import Fight


from lorgs import app as app_

app = app_.create_app()


WCL_CLIENT = WarcraftlogsClient.get_instance()


async def main():



    await WCL_CLIENT.update_auth_token()

    print(WCL_CLIENT.headers)

    # await test_1()
    # test_2()
    # await load_1()
    # test_2()

    # boss_slug = "painsmith-raznal"
    # spec_slug = "paladin-holy"
    # spec_ranking = warcraftlogs_ranking.SpecRanking.objects(boss_slug=boss_slug, spec_slug=spec_slug).first()
    # print(spec_ranking)
    # print(spec_ranking.spec)
    # print(spec_ranking.boss)
    # print(spec_ranking.boss.spells)


    report = warcraftlogs_report.Report()
    report.report_id = "ZtfLnQN8gDpw1cxR"

    fight = report.add_fight()
    fight.fight_id = 14
    fight.add_boss(2430)

    fight.start_time = 5143447

    with app.app_context():
        await fight.load()

    for cast in fight.boss.casts:
        print(cast, cast.spell.name)





if __name__ == '__main__':
    asyncio.run(main())
