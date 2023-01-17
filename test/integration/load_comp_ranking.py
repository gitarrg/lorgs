import dotenv


dotenv.load_dotenv()  # pylint: disable=wrong-import-position
import asyncio

from lorgs import data  # pylint: disable=unused-import
from lorgs.models.warcraftlogs_comp_ranking import CompRanking


async def test__load_rankings() -> None:
    comp_ranking = CompRanking(boss_slug="terros")
    # get_or_create

    # q = comp_ranking.get_query()
    # print(q)

    # x = comp_ranking.get_reports()
    # print(x)
    await comp_ranking.load(limit=3, clear_old=True)
    comp_ranking.save()

    for report in comp_ranking.reports:
        # print("R", report.report_id)
        for fight in report.fights:
            fight.players = []
            # print(fight.get_query())

            # print("\tF", fight.fight_id)
            # for player in fight.players:
            #     print("\t\tP", player.name, len(player.casts))


async def main() -> None:
    await test__load_rankings()


if __name__ == "__main__":
    asyncio.run(main())
