
# pylint: disable=wrong-import-position,invalid-name

# IMPORT STANDARD LIBRARIES
import os
import asyncio

# IMPORT THIRD PARTY LIBRARIES
import dotenv
dotenv.load_dotenv()

# IMPORT LOCAL LIBRARIES
from lorgs.app import create_app
from lorgs.models.specs import WowSpec, WowSpell
from lorgs.models.encounters import RaidZone, RaidBoss
from lorgs.models.reports import Player, Fight

from lorgs.db import db
from lorgs import client


# create app instance
app = create_app()
app.app_context().push()


async def test1():
    print("test1")

    # await WCL_CLIENT.update_auth_token()

    specs = WowSpec.query.all() # filter(WowSpec.name_slug_cap=="paladin-holy").all()

    boss = RaidBoss.query.filter_by(name="Hungering Destroyer").first()
    print("boss", boss)
    # boss = RaidBoss.query.filter_by(name="Shriekwing").first()

    # print(boss.fights)

    fights = boss.fights
    # fights = players.filter_by(spec=spec)

    players = Player.query
    players = players.join(Player.fight)
    players = players.join(Fight.boss)
    players = players.filter(Fight.boss == boss)
    players = players.all()

    """
    for player in players:
        print(player.fight.boss, player)
    """


    # return
    """
    warrior = WowClass.query.filter_by(name="Warrior").first()
    print(warrior)
    for spec in warrior.specs:
        print("\t", spec.full_name, spec.role)
    print("------------")

    print("SPECS:")
    for role in WowRole.query.all():
        print("\t", role)
        for spec in role.specs:
            print("\t\t", spec)
    """

async def test2():
    slug = "the-council-of-blood"

    print("_get_boss_by_slug", slug)
    for boss in RaidBoss.query.all():
        print("_get_boss_by_slug", slug, boss.name_slug)
        if boss.name_slug == slug:
            return boss


if __name__ == '__main__':
    asyncio.run(test1())
