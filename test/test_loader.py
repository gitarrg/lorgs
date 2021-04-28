# pylint: disable=wrong-import-position,invalid-name

# IMPORT STANDARD LIBRARIES
import os
import asyncio
import sqlalchemy

# IMPORT THIRD PARTY LIBRARIES
import dotenv
dotenv.load_dotenv()

from lorgs.app import create_app
from lorgs.client import WarcraftlogsClient
from lorgs.models import loader
from lorgs.models import Report
from lorgs.db import db

# client = WarcraftlogsClient

# create app instance
app = create_app()
app.app_context().push()

WCL_CLIENT = WarcraftlogsClient()


async def test_load_report():

    report_id = "tPNDbrzTVxH84XjB"

    print("########################")

    report = Report.query \
        .filter_by(report_id=report_id) \
        .options(sqlalchemy.orm.joinedload("fights")) \
        .options(sqlalchemy.orm.joinedload("fights.players")) \
        .options(sqlalchemy.orm.joinedload("fights.players.casts")) \
        .first()

    if not report:
        report = Report(report_id=report_id)

    # report.fights = []

    if not report.fights:
        await WCL_CLIENT.cache.load()
        report = await loader.load_report(report)

        for fight in report.fights:
            print(f"{fight} {fight.boss_id}")



        db.session.add(report)
        db.session.commit()
        await WCL_CLIENT.cache.save()

    else:
        print("LOADED")

    """
    print(report)
    # print(report.unique_players)
    # print(report.used_spells)
    for player in report.unique_players:
        print(player, player.used_spells)
    """
    print("DONE!")
    for fight in report.fights[:3]:
        print(f"{fight} {fight.percent:.1f}")

    """
    return
        print(f"\t{fight}")

        for player in fight.players:
            print(f"\t\t{player}")

    return
    """



if __name__ == '__main__':
    asyncio.run(test_load_report())
