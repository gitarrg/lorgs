
import dotenv
dotenv.load_dotenv() # pylint: disable=wrong-import-position

import asyncio
from lorgs.models import warcraftlogs_fight
from lorgs.models import warcraftlogs_report

from lorgs import data # pylint: disable=unused-import


def create_fight():
    report = warcraftlogs_report.Report(
        report_id="j68Fkv7DaVfmWbrc",
        start_time=1634490036325,
    )

    fight = warcraftlogs_fight.Fight(
        fight_id=8,
        start_time=1634490036325 + 5629191,
        duration=(6327948 - 5629191) / 1000,
        boss_id=2435,
    )
    fight.report = report

    return fight


async def load_fight_overview():
    """Load a fight that has no reference in our DB yet."""

    fight = create_fight()
    print(fight.get_summary_query())
    # await fight.load_overview()
    print(fight.players)


async def load_casts():

    fight = create_fight()

    await fight.load_overview()

    fight.players = fight.players[:3]
    fight.boss = None

    await fight.load_casts()




if __name__ == "__main__":
    asyncio.run(load_casts())
