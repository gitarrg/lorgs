
import asyncio
import pprint
import time

import dotenv
dotenv.load_dotenv() # pylint: disable=wrong-import-position
import mongoengine as me

from lorgs import db
# from lorgs import data
# from lorgs import utils
# from lorgs.app import create_app
# from lorgs.cache import Cache
# from lorgs.models.encounters import RaidBoss
# from lorgs.models.specs import WowSpec
# from lorgs.models.specs import WowSpell
# from lorgs.models import loader
from lorgs.models import warcraftlogs_ranking
# from lorgs import tasks


from lorgs.client import WarcraftlogsClient
C = WarcraftlogsClient.get_instance()
C.cached = False


async def test_1():

    from lorgs import data

    # warcraftlogs_ranking.SpecRanking.objects().delete()

    spec_slug = "demonhunter-vengeance"
    boss_slug = "test-boss"

    # for boss in data.CASTLE_NATHRIA_BOSSES:
    ranking = warcraftlogs_ranking.SpecRanking.get_or_create(boss_slug=boss_slug, spec_slug=spec_slug)
    await ranking.load(limit=5)
    ranking.save()


def load_1():

    spec_slug = "paladin-holy"
    boss_slug = "shriekwing"

    spec_ranking = warcraftlogs_ranking.SpecRanking.objects(boss_slug=boss_slug, spec_slug=spec_slug).first()
    print(spec_ranking)

    for spec_ranking in warcraftlogs_ranking.SpecRanking.objects:
        print(spec_ranking)

        # print(spec_ranking.reports)

        for player in spec_ranking.players:
            print(player.fight.report)
            print("\t", player.fight)
            print("\t\t", player)
            for cast in player.casts:
                print("\t\t\t", cast)

        # print(spec_ranking.fights)
        # print(spec_ranking.players)

        """
        for report in spec_ranking.reports:
            print("\t", report)
            for fight in report.fights:
                print("\t\t", fight)
                for player in fight.players:
                    print("\t\t\t", player)
                    for cast in player.casts:
                        print("\t\t\t\t", cast)
        """

def test_2():

    from lorgs import data
    from lorgs import tasks

    """
    spec_slug = "paladin-holy"
    boss_slug = "huntsman-altimor"
    tasks.load_spec_ranking(boss_slug=boss_slug, spec_slug=spec_slug)
    return
    """
    tasks.load_spec_ranking.delay(boss_slug="lady-inerva-darkvein", spec_slug="paladin-holy")
    # tasks.load_spec_ranking(boss_slug="lady-inerva-darkvein", spec_slug="holy-paladin")

    return
    for spec in data.SPECS:
        if not spec.supported:
            continue
        for boss in data.CASTLE_NATHRIA_BOSSES:
            spec_ranking = warcraftlogs_ranking.SpecRanking.objects(boss_slug=boss.name_slug, spec_slug=spec.full_name_slug).first()
            c = len(spec_ranking.reports) if spec_ranking else -1

            if c < 10:
                print(c, spec, boss)
                tasks.load_spec_ranking.delay(boss_slug=boss.name_slug, spec_slug=spec.full_name_slug)




async def main():
    await test_1()


if __name__ == '__main__':
    asyncio.run(main())
