
import dotenv
from lorgs.logger import timeit
dotenv.load_dotenv() # pylint: disable=wrong-import-position

import asyncio
from lorgs import data
from lorgs import db
from lorgs.models.warcraftlogs_user_report import UserReport


REPORT_ID = "J3tFdPDjaQnWVHfN"


async def test_load_summary():

    user_report = UserReport.from_report_id(report_id=REPORT_ID, create=True)

    # load
    await user_report.report.load_summary()

    # make sure things are loaded
    assert user_report.report.title == "Sanctum of Domination"
    assert len(user_report.report.players) == 20
    assert len(user_report.report.fights) > 0

    user_report.save()


async def test_load_fight_summary():

    user_report = UserReport.from_report_id(report_id=REPORT_ID)
    fight = user_report.report.get_fight(13)
    await fight.load_summary()
    user_report.save()


async def test_load_single_player():
    user_report = UserReport.from_report_id(report_id=REPORT_ID)
    fight = user_report.report.get_fight(13)
    player = fight.get_player(source_id=5)

    await player.load()
    print(player, player.casts)


async def test_load_multiple_players():

    user_report = UserReport.from_report_id(report_id=REPORT_ID)
    fight = user_report.report.get_fight(13)

    players = fight.get_players(source_ids=[2, 5, 8])

    for player in players:
        print(player, player.casts)

    await fight.load_many(players)

    for player in players:
        print(player, player.casts)
    # user_report.save()


async def test_load_multiple_fights():

    ids = range(1, 20)

    user_report = UserReport.from_report_id(report_id=REPORT_ID)
    await user_report.report.load_fights(
        fight_ids=ids,
        player_ids=[9]
    )

    @timeit
    async def save():
        user_report.save()

    await save()



async def test_load():

    user_report = UserReport.from_report_id(report_id=REPORT_ID, create=True)
    user_report.report.fights = []
    await user_report.report.load_fights(
        fight_ids=[35, 36],
        player_ids=[7, 8, 50, 53]
    )
    user_report.save()


async def main():
    # await test_load_summary()
    # await test_load_fight_summary()
    # await test_load_single_player()
    # await test_load_multiple_players()
    # await test_load_multiple_fights()
    await test_load()


if __name__ == "__main__":
    asyncio.run(main())
