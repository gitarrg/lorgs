

import asyncio

import dotenv
dotenv.load_dotenv()

from lorrgs_sqs.handler import load_user_report



async def test1() -> None:

    message = {
        'messageId': '23a984b5-1184-4e45-af1b-e926963a731f',
        'body': '{"task": "load_user_report", "report_id": "nMcmt14NG6wgB2QV", "user_id": 392483139991240714, "fight_ids": [1, 4, 10, 13, 17, 21, 27, 34], "player_ids": [1, 6, 15]}',
    }

    await load_user_report.main(message=message)


async def main():
    await test1()


if __name__ == "__main__":
    # loop = asyncio.get_event_loop()
    asyncio.run(main())


