# -*- coding: utf-8 -*-

# IMPORT STANDARD LIBRARIES
import os
import asyncio
import aiofiles
import shutil

# IMPORT THIRD PARTY LIBRARIES
import jinja2

# IMPORT LOCAL LIBRARIES
from wowtimeline import client
from wowtimeline import models
from wowtimeline import utils
from wowtimeline import wow_data


WCL_CLIENT_ID = "91c26642-e3e9-4090-945d-e65cf4720b5c"          # TODO: save as env vars
WCL_CLIENT_SECRET = "noOXQooD0qPXsXSPcnmluUElzT3tn2FR3GDviQbF"

GOOGLE_ANALYTICS_ID = "G-Y92VPCY6QW"


PWD = os.path.dirname(__file__)

TEMPLATE_FOLDER = os.path.join(PWD, "templates")
TEMPLATE_LOADER = jinja2.FileSystemLoader(searchpath=TEMPLATE_FOLDER)
TEMPLATE_ENV = jinja2.Environment(loader=TEMPLATE_LOADER)


# str: folder where the generated html files will be saved
OUTPUT_FOLDER = os.path.join(PWD, "../_build")


async def render(template_name, path, data):
    print("[RENDER]", path)

    # include some global args
    data["wow_data"] = wow_data
    data["GOOGLE_ANALYTICS_ID"] = GOOGLE_ANALYTICS_ID


    dirpath = os.path.dirname(path)
    if not os.path.exists(dirpath):
        print("[RENDER] creating folder:", dirpath)
        os.makedirs(dirpath)

    template = TEMPLATE_ENV.get_template(template_name)

    template.trim_blocks = True
    template.lstrip_blocks = True

    html = template.render(**data)
    async with aiofiles.open(path, 'w', encoding="utf-8") as f:
        await f.write(html)


async def main1():

    wcl_client = client.WarcraftlogsClient(client_id=WCL_CLIENT_ID, client_secret=WCL_CLIENT_SECRET)

    # fight = models.Fight("FytfnLWhGzBZ8cQM", 33)
    fight = models.Fight("hKFA382kt1cM6WZw", 26)
    fight.client = wcl_client
    await fight.fetch(
        spells=SPELLS
    )

    template = TEMPLATE_ENV.get_template("timeline.html")
    html = template.render(fight=fight)
    async with aiofiles.open("./test.html", 'w') as f:
        await f.write(html, encoding="utf-8")



WCL_CLIENT = client.WarcraftlogsClient(client_id=WCL_CLIENT_ID, client_secret=WCL_CLIENT_SECRET)


async def generate_ranking_report(boss, spec):

    fights = []
    """
    """
    fights = await WCL_CLIENT.get_top_ranks(boss["id"], spec)
    await WCL_CLIENT.cache.save()
    fights = fights[:50]

    await WCL_CLIENT.fetch_multiple_fights(fights)
    await WCL_CLIENT.cache.save()

    data = {}
    data["boss"] = boss
    data["spec"] = spec
    data["fights"] = fights
    path = f"{OUTPUT_FOLDER}/ranking_{spec.name_slug}_{boss['name_slug']}.html"
    await render("timeline.html", path, data)


async def generate_rankings():

    bosses = wow_data.ENCOUNTERS
    # bosses = wow_data.ENCOUNTERS[0:3]
    specs = [

        # healers
        wow_data.DRUID_RESTORATION,
        wow_data.PALADIN_HOLY,
        wow_data.PRIEST_DISCIPLINE,
        wow_data.PRIEST_HOLY,
        wow_data.SHAMAN_RESTORATION,

        # rdps
        wow_data.HUNTER_BEASTMASTERY,
        wow_data.HUNTER_MARKSMANSHIP,
        wow_data.MAGE_FIRE,
        wow_data.WARLOCK_AFFLICTION,
        wow_data.WARLOCK_DESTRUCTION,
    ]

    for spec in specs:
        print("GENERATE_RANKINGS", spec)
        for boss in bosses:
            print("GENERATE_RANKINGS", "Spec:", spec.full_name, "Boss:", boss["name"])
            await generate_ranking_report(boss, spec)


async def render_index():
    data = {}
    # we need smth to make the links work
    data["spec"] = wow_data.WARLOCK_AFFLICTION
    data["boss"] = wow_data.ENCOUNTERS[-1]

    path = f"{OUTPUT_FOLDER}/index.html"
    await render("index.html", path, data)


if __name__ == '__main__':
    asyncio.run(render_index())
    asyncio.run(generate_rankings())

