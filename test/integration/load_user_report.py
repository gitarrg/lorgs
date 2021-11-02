
import dotenv
dotenv.load_dotenv() # pylint: disable=wrong-import-position

import asyncio
from lorgs import data
from lorgs import db
from lorgs.models.warcraftlogs_user_report import UserReport


REPORT_ID = "j68Fkv7DaVfmWbrc"


async def test_load_summary():

    user_report = UserReport.from_report_id(report_id=REPORT_ID, create=True)

    # load
    await user_report.report.load_summary()

    # make sure things are loaded
    assert user_report.report.title == "Sanctum of Domination"
    assert len(user_report.report.players) == 20
    assert len(user_report.report.fights) == 21, user_report.report.fights

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

    user_report = UserReport.from_report_id(report_id=REPORT_ID)

    fights = user_report.report.get_fights(2, 4, 8)

    for fight in fights:
        print(fight)

    await user_report.report.load_many(fights)

    for fight in fights:
        print(fight)



async def test_load():

    user_report = UserReport.from_report_id(report_id=REPORT_ID)

    await user_report.report.load_fights(fight_ids=[2, 4, 8], player_ids=[3, 6, 9])



async def main():
    # await test_load_summary()
    # await test_load_fight_summary()
    # await test_load_single_player()
    # await test_load_multiple_players()
    # await test_load_multiple_fights()
    await test_load()


if __name__ == "__main__":
    asyncio.run(main())
