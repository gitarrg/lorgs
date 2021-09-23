#!/usr/bin/env python
"""Load a some test reports. Useful to assist in development."""

import asyncio

import dotenv
dotenv.load_dotenv() # pylint: disable=wrong-import-position

from lorgs import data
from lorgs import db
from lorgs.models import warcraftlogs_ranking
from lorgs.models import warcraftlogs_comps


########################################
#
#

async def load_spec_ranking():
    ########################################
    # Vars
    limit = 8
    boss = data.GUARDIAN
    spec = data.SHAMAN_RESTORATION

    ########################################
    # load
    ranking = warcraftlogs_ranking.SpecRanking.get_or_create(boss_slug=boss.name_slug, spec_slug=spec.full_name_slug)
    # for fight in ranking.fights:
    #     print(fight.get_query())
    #     break

    await ranking.load(limit=limit, clear_old=True)
    ranking.save()


async def load_comp():
    ########################################
    # Vars
    limit = 5
    boss = data.PAINSMITH
    comp_name = "any-heal"

    ########################################
    # load
    comp_config = warcraftlogs_comps.CompConfig.objects(name=comp_name).first()

    scr = await comp_config.load_reports(boss_slug=boss.name_slug, limit=limit)
    scr.save()
    comp_config.save()





async def main():
    await load_spec_ranking()


if __name__ == '__main__':
    asyncio.run(main())
