#!/usr/bin/env python
# IMPORT STANDARD LIBRARIES
import aiofiles
import asyncio
import json

# IMPORT THIRD PARTY LIBRARIES
import dotenv
dotenv.load_dotenv() # pylint: disable=wrong-import-position

# IMPORT LOCAL LIBRARIES
from lorgs.client import WarcraftlogsClient
from lorgs.logger import logger
from lorgs.models.specs import WowSpell
from lorgs import data
from lorgs import utils


filename = "spell_data.json"


async def load_spell_icons():

    spells = WowSpell.all
    spells = utils.uniqify(spells, lambda spell: spell.spell_id)
    logger.info("%d spells", len(spells))

    # Build query
    queries = [f"""
    gameData
    {{
        ability(id: {spell.spell_id}) {{name, icon}}
    }}
    """ for spell in spells]

    # run query
    wcl_client = WarcraftlogsClient.get_instance()
    data = await wcl_client.multiquery(queries)

    spell_info = {}

    # process data
    for spell, spell_data in zip(spells, data):
        spell_data = spell_data.get("ability", {})

        spell_info[spell.spell_id] = {}
        spell_info[spell.spell_id]["name"] = spell.spell_name or spell_data.get("name")
        spell_info[spell.spell_id]["icon"] = spell.icon_name or spell_data.get("icon")

    # save json
    async with aiofiles.open(filename, "w") as f:
        await f.write(json.dumps(spell_info, indent=4, sort_keys=True))


async def main():
    await load_spell_icons()





if __name__ == '__main__':
    asyncio.run(main())
