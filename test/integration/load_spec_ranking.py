
import dotenv
dotenv.load_dotenv() # pylint: disable=wrong-import-position
import asyncio


from lorgs import data  # pylint: disable=unused-import
from lorgs import db   # pylint: disable=unused-import

from lorgs.models.warcraftlogs_ranking import SpecRanking


async def test__load_rankings():
    # spec_ranking = SpecRanking.get_or_create(spec_slug="druid-restoration", boss_slug="painsmith-raznal")
    spec_ranking = SpecRanking.get_or_create(spec_slug="druid-restoration", boss_slug="fatescribe-rohkalo")
    # spec_ranking = SpecRanking.get_or_create(spec_slug="warlock-demonology", boss_slug="guardian-of-the-first-ones")

    await spec_ranking.load(limit=2, clear_old=True)

    spec_ranking.save()


async def main():
    await test__load_rankings()


if __name__ == "__main__":
    asyncio.run(main())
