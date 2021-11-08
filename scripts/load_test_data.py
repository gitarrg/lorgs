#!/usr/bin/env python
"""Load a some test reports. Useful to assist in development."""

import asyncio

import dotenv
dotenv.load_dotenv() # pylint: disable=wrong-import-position

from lorgs import data
from lorgs import db
from lorgs.models import warcraftlogs_ranking


########################################
#
#

async def load_spec_ranking():
    ########################################
    # Vars
    limit = 12
    boss = data.GUARDIAN
    spec = data.DRUID_RESTORATION

    ########################################
    # load
    ranking = warcraftlogs_ranking.SpecRanking.get_or_create(boss_slug=boss.full_name_slug, spec_slug=spec.full_name_slug)
    # for fight in ranking.fights:
    #     print(fight.get_query())
    #     break

    await ranking.load(limit=limit, clear_old=True)
    ranking.save()




async def main():
    await load_spec_ranking()


if __name__ == '__main__':
    asyncio.run(main())
