
import dotenv
dotenv.load_dotenv() # pylint: disable=wrong-import-position
import asyncio
import dataclasses


from lorgs import data  # pylint: disable=unused-import
from lorgs import db   # pylint: disable=unused-import

from lorgs.models.warcraftlogs_ranking import SpecRanking


TEMP_FILE = "/mnt/d/tmp.json"


async def test__load_rankings():
    # spec_ranking = SpecRanking.get_or_create(spec_slug="druid-restoration", boss_slug="fatescribe-rohkalo")
    # spec_ranking = SpecRanking.get_or_create(spec_slug="druid-restoration", boss_slug="painsmith-raznal")
    # spec_ranking = SpecRanking.get_or_create(spec_slug="druid-restoration", boss_slug="kelthuzad")
    # spec_ranking = SpecRanking.get_or_create(spec_slug="priest-discipline", boss_slug="sylvanas-windrunner")
    # spec_ranking = SpecRanking.get_or_create(spec_slug="warlock-demonology", boss_slug="guardian-of-the-first-ones")
    # spec_ranking = SpecRanking.get_or_create(spec_slug="paladin-holy", boss_slug="the-nine")
    # import dataclasses
    # dataclasses.asdict(cast)
    # print(cast, cast.dict())


    spec_ranking = SpecRanking(
        spec_slug="shaman-restoration",
        boss_slug="lords-of-dread",
        difficulty="heroic",
        metric="hps",
    )

    await spec_ranking.load(limit=10, clear_old=True)
    print(spec_ranking)
    print(spec_ranking.dict())
    print(spec_ranking.key)
    # spec_ranking.save()
    # spec_ranking.save()
    # return

    ##############
    # Additional Formatting
    # fights = spec_ranking.fights or []
    # result = {
    #     "updated": int(spec_ranking.updated.timestamp()),
    #     "difficulty": difficulty,
    #     "metric": metric,
    # }
    import json
    with open(TEMP_FILE, "w") as f:
        f.write(spec_ranking.json(exclude_unset=True, indent=None))
        # json.dump(, f, indent=4)


async def test__load_from_disk():

    spec_ranking = SpecRanking.parse_file(TEMP_FILE)
    spec_ranking.post_init()

    for report in spec_ranking.reports:
        print("R", report)
        for fight in report.fights.values():
            print("\tF", fight)
            for player in fight.players.values():
                print("\t\tP:", player)
                print(player.get_query())
            # print(fight.dict())
    # print(spec_ranking)
    # print(spec_ranking.dict())



async def test__load_from_db():

    spec_ranking = SpecRanking.get(
        spec_slug="druid-restoration",
        boss_slug="lords-of-dread",
        difficulty="heroic",
        metric="hps",
        create=True,
    )
    print(spec_ranking)
    spec_ranking.save()
    # await spec_ranking.load(limit=5, clear_old=True)


async def main():

    # pass
    # await test__load_rankings()
    # await test__load_from_disk()
    await test__load_from_db()


if __name__ == "__main__":
    # asyncio.run(main())
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    """
    try:
        loop.run_until_complete(main())
    finally:
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()
    """
