import asyncio
import itertools
import json

import dotenv

from lorgs.models import warcraftlogs_user_report
from lorgs.models.task import Task
from lorrgs_sqs.handler import load_user_report


dotenv.load_dotenv()


async def test1() -> None:

    # Inputs
    message_id = "23a984b5-1184-4e45-af1b-e926963a731f"
    REPORT_ID = "nMcmt14NG6wgB2QV"
    fight_ids = [1, 4, 10, 13, 17, 21, 27, 34]
    player_ids = [1, 6, 15]

    # delete old to force refresh
    user_report = warcraftlogs_user_report.UserReport.get_or_create(report_id=REPORT_ID)
    user_report.fights = []
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

    message = {"messageId": message_id, "body": json.dumps(body)}
    await load_user_report.main(message=message)


async def main() -> None:
    await test1()


if __name__ == "__main__":
    # loop = asyncio.get_event_loop()
    asyncio.run(main())
