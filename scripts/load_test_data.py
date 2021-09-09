"""Load a some test reports. Useful to assist in development."""

import asyncio

import dotenv
dotenv.load_dotenv() # pylint: disable=wrong-import-position

from lorgs import data
from lorgs.models import warcraftlogs_ranking


################################################################################

"""
_ref = GUARDIAN
TEST_BOSS = SANCTUM_OF_DOMINATION.add_boss(id=_ref.id, name="Test Boss")
TEST_BOSS.visible = False
TEST_BOSS.events = _ref.events
TEST_BOSS.spells = _ref.spells


spec_slug = "demonhunter-vengeance"
boss_slug = "test-boss"
limit = 5



#
boss.name = "test"
spec.name = "test"
"""



########################################
#
#

async def main():
    print(1)

    ########################################
    # Vars
    limit = 5
    boss = data.KELTHUZAD
    spec = data.DRUID_RESTORATION

    ########################################
    # load
    ranking = warcraftlogs_ranking.SpecRanking.get_or_create(boss_slug=boss.name_slug, spec_slug=spec.full_name_slug)
    for fight in ranking.fights:
        print(fight.get_query())
        break

    await ranking.load(limit=limit)

    # ranking.
    ranking.save()
    # print(ranking)


if __name__ == '__main__':
    asyncio.run(main())
