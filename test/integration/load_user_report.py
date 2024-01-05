from pprint import pprint
import re
import dotenv

from lorgs.logger import timeit


dotenv.load_dotenv()  # pylint: disable=wrong-import-position

import asyncio

from lorgs import data
from lorgs.models.warcraftlogs_user_report import UserReport


TEMP_FILE = "/mnt/d/tmp.json"


REPORT_ID = "4KZGNP8HtxWRkyJ9"
# https://www.warcraftlogs.com/reports/PHjzrwW6Y2vTdbMJ#fight=11&type=damage-done


async def test_load_summary():
    user_report = UserReport(report_id=REPORT_ID)

    # load
    await user_report.load_summary()

    # make sure things are loaded
    # assert user_report.title == "Farm #9"
    # assert len(user_report.players) == 20
    # assert len(user_report.fights) > 0

    user_report.save()
    # user_report.save(filename=TEMP_FILE, indent=4)


@timeit
async def test_load_fight_summary():
    user_report = UserReport.get(report_id=REPORT_ID)
    fight = user_report.report.get_fight(13)
    await fight.load_summary()
    user_report.save()


async def test_load_single_player():
    user_report = UserReport.get(report_id=REPORT_ID)
    fight = user_report.report.get_fight(13)
    player = fight.get_player(source_id=5)

    await player.load()
    print(player, player.casts)


async def test_load_multiple_players():
    user_report = UserReport.get(report_id=REPORT_ID)
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
    await user_report.report.load_fights(fight_ids=ids, player_ids=[9])

    @timeit
    async def save():
        user_report.save()

    await save()


def info_from_url(url: str) -> tuple[str, int, int]:
    report_id_match = re.search(r"reports\/(\w{16})", url)
    fight_id_match = re.search(r"fight=(\d+)", url)
    player_id_match = re.search(r"source=(\d+)", url)

    report_id = report_id_match.group(1) if report_id_match else ""
    fight_id = int(fight_id_match.group(1)) if fight_id_match else -1
    player_id = int(player_id_match.group(1)) if player_id_match else -1

    return (report_id, fight_id, player_id)


async def test_load() -> None:
    url = "https://www.warcraftlogs.com/reports/tbyNhJqMmGzYKHnk#fight=17&player=4"
    REPORT_ID, fight_id, player_id = info_from_url(url)
    fight_ids = [fight_id]
    player_ids = [player_id]

    # LOAD
    user_report = UserReport.get_or_create(report_id=REPORT_ID, create=True)

    # for fight in user_report.fights:
    #     print(fight.duration, type(fight.duration))

    await user_report.load()
    # user_report.players = []
    # user_report.fights = []
    # user_report.save()
    # print(user_report.dict())

    # return
    # user_report.post_init()

    # print(user_report.get_query())
    # user_report.fights = []
    await user_report.load_fights(fight_ids=fight_ids, player_ids=player_ids)
    user_report.save()

    # for fight in user_report.fights:
    #     for player in fight.players:
    #         print(player.dict())
    #         return

    ############################
    # Print Result
    #
    def f(l, j="."):
        l = [str(i) for i in l]
        return j.join(l)

    fight_ids = f(fight_ids)
    player_ids = f(player_ids)
    print(f"http://localhost:9001/user_report/{REPORT_ID}?fight={fight_ids}&player={player_ids}")


async def test_load_with_progress() -> None:
    import itertools

    from lorgs.models.task import Task

    task = Task.get_or_create(task_id="dev")
    # task.items["1.5"]["status"] = Task.STATUS.IN_PROGRESS

    # task.set("items.1_5", {"status": "changed"})
    # task.set("items.1_5.status", "changed9")

    REPORT_ID = "QYvHMnjhy9x6dZg4"
    FIGHT_IDS = [25]
    PLAYER_IDS = [14]

    ################################
    # Create Status Object
    task = Task(task_id="dev", status=Task.STATUS.WAITING)
    task.items = {}
    for f, p in itertools.product(FIGHT_IDS, PLAYER_IDS):
        task.items[f"{f}_{p}"] = {"fight": f, "player": p, "status": task.status}
    task.save()

    ################################
    # Main
    user_report = UserReport.get_or_create(report_id=REPORT_ID)
    await user_report.load_fights(fight_ids=FIGHT_IDS, player_ids=PLAYER_IDS)


async def main() -> None:
    # await test_load_summary()
    # await test_load_fight_summary()
    # await test_load_single_player()
    # await test_load_multiple_players()
    # await test_load_multiple_fights()
    await test_load()
    # await test_load_with_progress()


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
