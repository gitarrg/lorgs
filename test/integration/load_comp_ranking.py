import dotenv


dotenv.load_dotenv()  # pylint: disable=wrong-import-position
import asyncio

from lorgs import data  # pylint: disable=unused-import
from lorgs.models.warcraftlogs_comp_ranking import CompRanking


async def test__load_rankings() -> None:
    comp_ranking = CompRanking.get_or_create(boss_slug="eranog")
    await comp_ranking.load(page=1, clear_old=False)
    comp_ranking.save()


async def main() -> None:
    await test__load_rankings()


if __name__ == "__main__":
    asyncio.run(main())
