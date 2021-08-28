#!/usr/bin/env python
# IMPORT STANDARD LIBRARIES
import asyncio

# IMPORT THIRD PARTY LIBRARIES
import dotenv
dotenv.load_dotenv() # pylint: disable=wrong-import-position

# IMPORT LOCAL LIBRARIES
from lorgs.client import WarcraftlogsClient


spells = [
    6262,
    307192,
    345019,
    349857,
    330323,
    345539,
    348139,
    345228,
    345801,
    345251,
    345530,
    345251,
]

async def load_spell_icons():

    # Build query
    queries = [f"""
    gameData
    {{
        ability(id: {spell}) {{name, icon}}
    }}
    """ for spell in spells]

    # run query
    wcl_client = WarcraftlogsClient.get_instance()
    data = await wcl_client.multiquery(queries)

    # process data
    for spell, spell_data in zip(spells, data):
        spell_data = spell_data.get("ability", {})
        print(f'{spell}: name="{spell_data["name"]}", icon="{spell_data["icon"]}"')



async def main():
    await load_spell_icons()




if __name__ == '__main__':
    asyncio.run(main())
