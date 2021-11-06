
import dotenv
dotenv.load_dotenv() # pylint: disable=wrong-import-position

import asyncio
from lorgs.models.warcraftlogs_report import Report


async def test_load_master_data():

    report = Report(report_id="j68Fkv7DaVfmWbrc")

    # make sure its empty
    assert not report.title
    assert not report.players
    assert not report.fights

    # load
    await report.load()

    # make sure things are loaded
    assert report.title == "Sanctum of Domination"
    assert len(report.players) == 20
    assert len(report.fights) == 21, report.fights


async def test_load_fight():

    report = Report(report_id="j68Fkv7DaVfmWbrc")

    fight_data = {'id': 13, 'encounterID': 2435, 'startTime': 9305239, 'endTime': 9539568}
    report.add_fight(**fight_data)

    fight = report.get_fight(13)
    await fight.load()
    print(fight)


async def main():
    await test_load_master_data()
    # await test_load_fight()


if __name__ == "__main__":
    asyncio.run(main())
    # asyncio.run(load_casts())
