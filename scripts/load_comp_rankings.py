#!/usr/bin/env python
"""Python Script to load Comp Ranking Data."""

import asyncio

import dotenv
dotenv.load_dotenv() # pylint: disable=wrong-import-position

from lorgs import data
from lorgs import db  # needs to be imported to setup the default connection
from lorgs.models import warcraftlogs_comp_ranking
# from lorgs.models import warcraftlogs_ranking




async def load_boss(boss_slug, limit=10, clear_old=False):
    print(f"load START {boss_slug} (limit={limit})")

    comp_ranking = warcraftlogs_comp_ranking.CompRanking(boss_slug=boss_slug)
    await comp_ranking.update_reports(limit=limit, clear_old=clear_old)
    comp_ranking.save()
    print(f"load DONE {boss_slug} (limit={limit})")


async def load_all_bosses(limit=10, clear_old=False):

    for boss in data.SANCTUM_OF_DOMINATION_BOSSES:
        await load_boss(boss.full_name_slug, limit=limit, clear_old=clear_old)
        # boss.full_name_slug for 


async def main():
    await load_all_bosses(limit=10)
    # await load_boss("the-tarragrue")


if __name__ == "__main__":
    asyncio.run(main())
