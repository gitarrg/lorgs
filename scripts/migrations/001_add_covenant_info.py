#!/usr/bin/env python
"""Util to fill in some missing data."""

import asyncio
import os

import dotenv
dotenv.load_dotenv() # pylint: disable=wrong-import-position
os.environ["MONGO_URI"] = os.getenv("MONGO_URI_PROD") # pylint: disable=wrong-import-position

from lorgs import data
from lorgs import db
from lorgs.models import warcraftlogs_ranking

########################################
#
#

async def load_one_spec_ranking(boss, spec, limit=5):

    print("loading", boss, "vs", spec)
    old_ranking = warcraftlogs_ranking.SpecRanking.get_or_create(boss_slug=boss.name_slug, spec_slug=spec.full_name_slug)

    def rkey(ranking):
        """Unique Key to identify the report/fight/player."""
        return (
            ranking.get("report", {}).get("code"),
            ranking.get("report", {}).get("fightID"),
            ranking.get("name", ""),
        )

    # query rankings and group them
    rankings = await old_ranking.load_rankings(limit=limit)
    rankings = {rkey(r): r for r in rankings}

    # loop over old reports, try to match the keys and set the new ids
    for player in old_ranking.players:

        # key
        k = (player.fight.report.report_id, player.fight.fight_id, player.name)

        # new data
        d = rankings.get(k)
        if d:
            player.covenant_id = d.get("covenantID")
            player.soulbind_id = d.get("soulbindID")

    # await ranking.load(limit=limit, clear_old=True)
    old_ranking.save()


async def load_spec_ranking():
    ########################################
    # Vars
    limit = 60
    bosses = data.SANCTUM_OF_DOMINATION.bosses[1:]
    specs = data.SPECS
        
    for boss in bosses:
        # tasks = []
        for spec in specs:
            await load_one_spec_ranking(boss, spec, limit=limit)
        # await asyncio.gather(*tasks)


async def remove_invalid():
    bosses = data.SANCTUM_OF_DOMINATION.bosses
    specs = data.SPECS

    # bosses = [data.GUARDIAN]
    # specs = [data.DEATHKNIGHT_BLOOD]

    def keep(report):
        for fight in report.fights:
            for player in fight.players:
                if player.covenant_id != None:
                    return True
        return False


    for boss in bosses:
        for spec in specs:

            ranking = warcraftlogs_ranking.SpecRanking.get_or_create(boss_slug=boss.name_slug, spec_slug=spec.full_name_slug)


            # await ranking.load(limit=50, clear_old=False)
            print(len(ranking.players))

            # x = [p for p in ranking.players if p.covenant_id == None]
            # print(boss.name_slug, spec.full_name_slug, len(x), [p.name for p in x])

            ranking.reports = [r for r in ranking.reports if keep(r)]
            print(len(ranking.players))
            ranking.save()


async def main():
    # await load_spec_ranking()
    # await load_one_spec_ranking(data.PAINSMITH, data.DEATHKNIGHT_UNHOLY)
    await remove_invalid()


if __name__ == '__main__':
    asyncio.run(main())
