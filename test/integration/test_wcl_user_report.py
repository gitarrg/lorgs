"""Test the Model and Functions related to User Reports."""
import os
import dotenv
import asyncio

dotenv.load_dotenv() # pylint: disable=wrong-import-position

PWD = os.path.dirname(__file__)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.abspath(f"{PWD}/../../google_creds.json")


from lorgs import db # pylint: disable=unused-import
from lorgs import data  # pylint: disable=unused-import
from lorgs.models.warcraftlogs_user_report import UserReport
from lorgs.routes.api_tasks import create_cloud_function_task


TEST_REPORT_ID = ""  # add some report ID for testing


################################################


async def test_load_report_overview():
    user_report = UserReport.from_report_id(TEST_REPORT_ID)
    # print(user_report)
    await user_report.load()
    # print(user_report.report)
    # for fight in user_report.report.fights:
    #     print("\t", fight)
    #     print("\t", fight.duration)
    # print(user_report.report._players)
    user_report.save()


async def test_load_report():
    fight_ids = [15, 19, 22]
    player_ids = [2, 7, 23, 55, 60,]

    user_report = UserReport.from_report_id(TEST_REPORT_ID, create=True)
    print("user_report", user_report)

    await user_report.report.load_fights(fight_ids=fight_ids, player_ids=player_ids)
    for fight in user_report.report.fights.values():
        print("Fight:", fight)
        for player in fight.players:
            print("\t", player, player.casts)


    user_report.save()


async def load_via_gcf():
    task_id = await create_cloud_function_task(
        "load_user_report",
        report_id=TEST_REPORT_ID,
        fight=[3, 4, 5, 6],
        player=[3, 6, 11, 13]
    )
    print("task id", task_id)



if __name__ == '__main__':
    # unittest.main()
    # asyncio.run(test_load_report_overview())
    asyncio.run(test_load_report())
    # asyncio.run(load_via_gcf())
