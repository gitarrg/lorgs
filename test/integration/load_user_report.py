
import dotenv
from lorgs.logger import timeit
dotenv.load_dotenv() # pylint: disable=wrong-import-position

import asyncio
from lorgs import data
from lorgs import db
from lorgs.models.warcraftlogs_user_report import UserReport


REPORT_ID = "N3FyfmBCcbqXVk2h"
# https://www.warcraftlogs.com/reports/PHjzrwW6Y2vTdbMJ#fight=11&type=damage-done


async def test_load_summary():

    user_report = UserReport.from_report_id(report_id=REPORT_ID, create=True)

    # load
    await user_report.report.load_summary()

    # make sure things are loaded
    assert user_report.report.title == "Sanctum of Domination"
    assert len(user_report.report.players) == 20
    assert len(user_report.report.fights) > 0

    user_report.save()


@timeit
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


from lorgs import events

async def test_load() -> None:

    REPORT_ID = "LAjpTGtv7FZrP9YH"
    fight_ids = [2, 3, 4, 6, 7]
    player_ids = [3, 8, 5]

    # Setup test handler
    progress = {
        "done": 0,
        "steps": len(fight_ids) * (len(player_ids) + 1 + 1),
    }

    async def increase_done(event: events.Event) -> None:
        actor = event.payload.get("actor")
        print("actor", actor)
        progress["done"] += 1

    # async def report_status(event) -> None
    #     print(f"Progress: {d}/{t} ({d/t:.1%})")

    events.register("player.load.complete", increase_done)
    # events.register("boss.load.complete", increase_done)
    # events.register("actor.load.complete", report_status)


    user_report = UserReport.from_report_id(report_id=REPORT_ID, create=True)
    user_report.report.fights = {}
    await user_report.report.load_fights(fight_ids=fight_ids, player_ids=player_ids)
    return 
    user_report.save()

    ############################
    # Print Result
    #
    def f(l, j="."):
        l = [str(i) for i in l]
        return j.join(l)

    fight_ids = f(fight_ids)
    player_ids = f(player_ids)
    print(f"http://localhost:9001/user_report/{REPORT_ID}?fight={fight_ids}&player={player_ids}")



    # Add subitems to track the status more granual
    for (f, p) in itertools.product(fight_ids, player_ids):
        task.items[f"{f}.{p}"] = {"fight": f, "player": p, "status": task.status}


async def test_load_with_progress() -> None:
    from lorgs.models.task import Task
    import itertools
    import typing
    from lorgs.models import warcraftlogs_actor


    task = Task.get(key="dev")
    # task.items["1.5"]["status"] = Task.STATUS.IN_PROGRESS

    # task.set("items.1_5", {"status": "changed"})
    task.set("items.1_5.status", "changed9")

    REPORT_ID = "LAjpTGtv7FZrP9YH"
    FIGHT_IDS = [2, 3, 4, 6, 7, 8, 9]
    PLAYER_IDS = [3, 8, 5, 1, 2, 3, 4]

    ################################
    # Create Status Object
    task = Task(key="dev", status=Task.STATUS.WAITING)
    task.items = {}
    for (f, p) in itertools.product(FIGHT_IDS, PLAYER_IDS):
        task.items[f"{f}_{p}"] = {"fight": f, "player": p, "status": task.status}
    task.save()

    ################################
    # Main
    user_report = UserReport.from_report_id(report_id=REPORT_ID, create=True)
    await user_report.report.load_fights(
        fight_ids=FIGHT_IDS,
        player_ids=PLAYER_IDS
    )



async def main():



    # await test_load_summary()
    # await test_load_fight_summary()
    # await test_load_single_player()
    # await test_load_multiple_players()
    # await test_load_multiple_fights()
    # await test_load()
    await test_load_with_progress()


if __name__ == "__main__":
    # loop = asyncio.get_event_loop()
    asyncio.run(main())

    """
    loop = asyncio.new_event_loop()

    # print(loop.is_closed())
    try:
        loop.run_until_complete(main())
    finally:
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()
    """
