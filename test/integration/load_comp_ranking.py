
import dotenv
dotenv.load_dotenv() # pylint: disable=wrong-import-position
import asyncio


from lorgs import data  # pylint: disable=unused-import
from lorgs import db   # pylint: disable=unused-import

from lorgs.models.warcraftlogs_comp_ranking import CompRanking


async def test__load_rankings():
    comp_ranking = CompRanking.get_or_create(boss_slug="guardian-of-the-first-ones")

    # x = comp_ranking.get_reports()
    # print(x)
    await comp_ranking.load(limit=5, clear_old=True)
    comp_ranking.save()


async def main():
    await test__load_rankings()


if __name__ == "__main__":
    asyncio.run(main())
