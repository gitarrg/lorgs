
# pylint: disable=wrong-import-position,invalid-name

# IMPORT STANDARD LIBRARIES
import os
import asyncio

# IMPORT THIRD PARTY LIBRARIES
import dotenv
dotenv.load_dotenv()

# IMPORT LOCAL LIBRARIES
from lorgs.app import create_app
from lorgs.models.specs import WowSpec, WowSpell
# from lorgs.models.encounters import RaidZone, RaidBoss
from lorgs.models import reports

from lorgs.db import db
from lorgs import client


REPORT_ID = "KQBbcGCyX87L92NR"
FIGHT = 7
source=20


# create app instance
app = create_app()
app.app_context().push()


WCL_CLIENT_ID = os.getenv("WCL_CLIENT_ID")
WCL_CLIENT_SECRET = os.getenv("WCL_CLIENT_SECRET")
WCL_CLIENT = client.WarcraftlogsClient(client_id=WCL_CLIENT_ID, client_secret=WCL_CLIENT_SECRET)


def _init_db():
    db.create_all()
    db.session.commit()


async def test1():

    # await WCL_CLIENT.update_auth_token()

    report = db.get_or_create(reports.Report, report_id=REPORT_ID)
    print("report", report)
    # db.session.delete(report)
    # db.session.commit()

    if report.fights:
        db.session.delete(report.fights)
        db.session.commit()

    if not report.fights:
        await report.fetch_fights(WCL_CLIENT)

    spells = WowSpell.query.all()
    fights = report.fights[:1]
    await WCL_CLIENT.fetch_multiple_fights(fights, spells=spells)


    print(report)
    for fight in report.fights:
        print("\t", fight)

        for player in fight.players:
            print("\t\t", player)

    db.session.commit()
    # return
    """
    warrior = WowClass.query.filter_by(name="Warrior").first()
    print(warrior)
    for spec in warrior.specs:
        print("\t", spec.full_name, spec.role)
    print("------------")

    print("SPECS:")
    for role in WowRole.query.all():
        print("\t", role)
        for spec in role.specs:
            print("\t\t", spec)
    """



if __name__ == '__main__':
    _init_db()
    asyncio.run(test1())
