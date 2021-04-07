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


PWD = os.path.dirname(__file__)

TEMPLATE_FOLDER = os.path.join(PWD, "templates")
TEMPLATE_LOADER = jinja2.FileSystemLoader(searchpath=TEMPLATE_FOLDER)
TEMPLATE_ENV = jinja2.Environment(loader=TEMPLATE_LOADER)


# str: folder where the generated html files will be saved
OUTPUT_FOLDER = os.path.join(PWD, "../_build")


async def render(path, data):
    print("[RENDER]", path)


    dirpath = os.path.dirname(path)
    if not os.path.exists(dirpath):
        print("[RENDER] creating folder:", dirpath)
        os.makedirs(dirpath)

    template = TEMPLATE_ENV.get_template("timeline.html")

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

    fights = await WCL_CLIENT.get_top_ranks(boss["id"], spec)
    await WCL_CLIENT.cache.save()
    fights = fights[:5]

    await WCL_CLIENT.fetch_multiple_fights(fights)
    await WCL_CLIENT.cache.save()

    data = {}
    data["wow_data"] = wow_data
    data["boss"] = boss
    data["spec"] = spec
    data["fights"] = fights
    path = f"{OUTPUT_FOLDER}/rankings/{boss['name_slug']}_{spec.name_slug}.html"
    await render(path, data)


async def generate_rankings(bosses, specs):
    for boss in bosses:
        for spec in specs:
            print("Boss:", boss["name"], "Spec:", spec.full_name)
            await generate_ranking_report(boss, spec)


async def main2():


    """
    for wow_class in wow_data.CLASSES.values():
        for i, spec in wow_class.specs.items():
            print(i, spec)
    """

    bosses = [wow_data.ENCOUNTERS[7], wow_data.ENCOUNTERS[9]]
    specs = [
        wow_data.MAGE_FIRE,
        wow_data.WARLOCK_AFFLICTION,
        wow_data.PALADIN_HOLY
    ]
    await generate_rankings(bosses, specs)

    #####
    # Copy static folder
    # static_src = os.path.join(PWD, "static")
    # static_tar = os.path.join(OUTPUT_FOLDER, "static")
    # if os.path.exists(static_tar):
    #     shutil.rmtree(static_tar)
    # shutil.copytree(static_src, static_tar)



    return

    boss = wow_data.ENCOUNTERS[7]
    spec = wow_data.DRUID_RESTORATION



    return
    """
    for toplog in rankings:
        # fight = models.Fight(fight_data["reportID"], fight_data["fightID"])
        print(toplog["reportID"], toplog["fightID"], toplog["name"])
    """


if __name__ == '__main__':
    # print(PWD)
    asyncio.run(main2())


