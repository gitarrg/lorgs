
# IMPORT STANDARD LIBRARIES
import asyncio

import dotenv
dotenv.load_dotenv()

# IMPORT THIRD PARTY LIBRARIES
from lorgs.app import create_app
from lorgs.cache import Cache
from lorgs.client import WarcraftlogsClient
from lorgs.logger import logger
from lorgs.models import loader
from lorgs import data
from lorgs.models.encounters import RaidBoss
from lorgs.models.specs import WowClass
from lorgs.models.specs import WowSpec
from lorgs.models.specs import WowSpell


WCL_CLIENT = WarcraftlogsClient.get_instance()


async def load_spell_data():

    spells = {spell.spell_id: spell for spell in WowSpell.all}
    logger.info("%d spells", len(spells))

    # Build query
    queries = [f"spell_{spell_id}: ability(id: {spell_id}) {{id, name, icon}}" for spell_id in spells.keys()]
    queries = "\n".join(queries)
    query = f"""
    gameData
    {{
        {queries}
    }}
    """
    data = await WCL_CLIENT.query(query)
    data = data.get("gameData", {})

    # save cache
    spell_infos = {info.pop("id"): info for info in data.values()}
    Cache.set("spell_infos", spell_infos, timeout=0)


async def load_one_char_rankings(spec, boss, limit=0):

    key = f"char_rankings/{spec.full_name_slug}/boss={boss.name_slug}"
    logger.info(key)
    players = await loader.load_char_rankings(boss=boss, spec=spec, limit=limit)

    # we always cache from report level
    reports = [player.fight.report for player in players]
    Cache.set(key, reports, timeout=0)


async def load_all_char_rankings(specs=None, bosses=None, limit=0):
    logger.info(f">>>>>>> START <<<<<<<<")

    specs = specs or data.SPECS
    specs = [spec for spec in specs if spec.supported]
    specs = [WowSpec.get(full_name_slug="druid-restoration")]

    bosses = bosses or data.BOSSES
    bosses = list(bosses)[:2]

    for spec in specs:
        tasks = [load_one_char_rankings(spec, boss, limit=limit) for boss in bosses]
        await asyncio.gather(*tasks)



async def main():
    app = create_app()
    with app.app_context():
        await load_all_char_rankings(limit=10)


if __name__ == '__main__':
    asyncio.run(main())
