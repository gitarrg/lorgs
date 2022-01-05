
import dotenv
dotenv.load_dotenv() # pylint: disable=wrong-import-position
import asyncio


from lorgs import data  # pylint: disable=unused-import
from lorgs import db   # pylint: disable=unused-import

from lorgs.models.warcraftlogs_ranking import SpecRanking


async def test__load_rankings():
    spec_ranking = SpecRanking.get_or_create(spec_slug="druid-restoration", boss_slug="fatescribe-rohkalo")
    spec_ranking = SpecRanking.get_or_create(spec_slug="druid-restoration", boss_slug="painsmith-raznal")
    spec_ranking = SpecRanking.get_or_create(spec_slug="druid-restoration", boss_slug="kelthuzad")
    spec_ranking = SpecRanking.get_or_create(spec_slug="priest-discipline", boss_slug="sylvanas-windrunner")
    # spec_ranking = SpecRanking.get_or_create(spec_slug="warlock-demonology", boss_slug="guardian-of-the-first-ones")
    spec_ranking = SpecRanking.get_or_create(spec_slug="paladin-holy", boss_slug="the-nine")

    await spec_ranking.load(limit=20, clear_old=True)
    spec_ranking.save()


async def test__load_all_rankings():

    spec_slug = "druid-restoration"

    for boss in data.CURRENT_ZONE.bosses:
        spec_ranking = SpecRanking.get_or_create(spec_slug=spec_slug, boss_slug=boss.full_name_slug)
        await spec_ranking.load(limit=5, clear_old=True)
        spec_ranking.save()


async def main():
    await test__load_rankings()
    # await test__load_all_rankings()


if __name__ == "__main__":
    asyncio.run(main())
