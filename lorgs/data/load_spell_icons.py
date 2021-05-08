#!/usr/bin/env python
# IMPORT STANDARD LIBRARIES
import asyncio

# IMPORT THIRD PARTY LIBRARIES

# IMPORT LOCAL LIBRARIES
from lorgs.client import WarcraftlogsClient
from lorgs import db
from lorgs.logger import logger
from lorgs.models.specs import WowSpell


async def load_spell_icons():

    spells = WowSpell.query.all()
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

    # process data
    for spell, spell_data in zip(spells, data):
        spell_data = spell_data.get("ability", {})
        spell.spell_name = spell.spell_name or spell_data.get("name")
        spell.icon_name = spell.icon_name or spell_data.get("icon")



async def main():
    with db.session_context(commit=True):
        await load_spell_icons()


if __name__ == '__main__':
    asyncio.run(main())
