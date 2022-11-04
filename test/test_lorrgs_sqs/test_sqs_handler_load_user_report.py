

import asyncio
import json
import itertools


import dotenv
dotenv.load_dotenv()

from lorgs.models import warcraftlogs_user_report
from lorrgs_sqs.handler import load_user_report
from lorgs.models.task import Task



async def test1() -> None:

    # Inputs
    message_id = "23a984b5-1184-4e45-af1b-e926963a731f"
    REPORT_ID = "nMcmt14NG6wgB2QV"
    fight_ids = [1, 4, 10, 13, 17, 21, 27, 34]
    player_ids = [1, 6, 15]

    # delete old to force refresh
    user_report = warcraftlogs_user_report.UserReport.from_report_id(report_id=REPORT_ID, create=True)
    user_report.report.fights = {}
    user_report.save()

    # setup Task object
    task = Task(key=message_id, status=Task.STATUS.WAITING)
    for (f, p) in itertools.product(fight_ids, player_ids):
        task.items[f"{f}_{p}"] = {"fight": f, "player": p, "status": task.status}
    task.save()

    # Main
    body = {
        "task": "load_user_report",
        "report_id": REPORT_ID,
        "fight_ids": fight_ids,
        "player_ids": player_ids,
    }

    message = {
        'messageId': message_id,
        'body': json.dumps(body)
    }
    await load_user_report.main(message=message)


async def main():
    await test1()


if __name__ == "__main__":
    # loop = asyncio.get_event_loop()
    asyncio.run(main())


