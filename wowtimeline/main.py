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
from wowtimeline.logger import logger


WCL_CLIENT_ID = "91c26642-e3e9-4090-945d-e65cf4720b5c"          # TODO: save as env vars
WCL_CLIENT_SECRET = "noOXQooD0qPXsXSPcnmluUElzT3tn2FR3GDviQbF"

GOOGLE_ANALYTICS_ID = "G-Y92VPCY6QW"


PWD = os.path.dirname(__file__)

TEMPLATE_FOLDER = os.path.join(PWD, "templates")
TEMPLATE_LOADER = jinja2.FileSystemLoader(searchpath=TEMPLATE_FOLDER)
TEMPLATE_ENV = jinja2.Environment(loader=TEMPLATE_LOADER)
TEMPLATE_ENV.trim_blocks = True
TEMPLATE_ENV.lstrip_blocks = True

# TEMPLATE_ENV.filters["slug"] = utils.slug

# str: folder where the generated html files will be saved
OUTPUT_FOLDER = os.path.join(PWD, "../_build")

DEBUG = os.getenv("DEBUG")


WCL_CLIENT = client.WarcraftlogsClient(client_id=WCL_CLIENT_ID, client_secret=WCL_CLIENT_SECRET)

################################################################################
#   Jinja
#

async def render(template_name, path, data):
    # print("[RENDER]", path)

    # include some global args
    data["wow_data"] = wow_data
    data["GOOGLE_ANALYTICS_ID"] = GOOGLE_ANALYTICS_ID

    dirpath = os.path.dirname(path)
    if not os.path.exists(dirpath):
        logger.info("creating folder:", dirpath)
        os.makedirs(dirpath)

    template = TEMPLATE_ENV.get_template(template_name)

    html = template.render(**data)
    async with aiofiles.open(path, 'w', encoding="utf-8") as f:
        await f.write(html)


async def render_index():
    data = {}
    # we need smth to make the links work
    data["spec"] = wow_data.WARLOCK_AFFLICTION
    data["boss"] = wow_data.ENCOUNTERS[-1]

    path = f"{OUTPUT_FOLDER}/index.html"
    await render("index.html", path, data)

################################
#       Rankings
#

async def generate_ranking_report(boss, spec):

    # points_before = await WCL_CLIENT.get_points_left()

    fights = []
    fights = await WCL_CLIENT.get_top_ranks(boss["id"], spec)
    fights = fights[:25] # limit a bit for now
    # if DEBUG:
    #     fights = fights[:2]

    tasks = [f.fetch(WCL_CLIENT) for f in fights]
    tasks = [asyncio.create_task(t) for t in tasks]
    await asyncio.gather(*tasks)

    data = {}
    data["boss"] = boss
    data["spec"] = spec
    data["all_spells"] = spec.spells.values()
    data["fights"] = fights
    path = f"{OUTPUT_FOLDER}/rankings_{spec.full_name_slug}_{boss['name_slug']}.html"
    await render("ranking.html", path, data)

    logger.info(f"[GENERATED REPORT] {spec.full_name} vs {boss['name']}")
    return


async def generate_rankings():
    bosses = wow_data.ENCOUNTERS
    specs = wow_data.SPECS_SUPPORTED

    if DEBUG:
        bosses = [wow_data.ENCOUNTERS[-1]]
        specs = [
            # healers
            # wow_data.DRUID_RESTORATION,
            # wow_data.PALADIN_HOLY,
            # wow_data.PRIEST_DISCIPLINE,
            # wow_data.PRIEST_HOLY,
            # wow_data.SHAMAN_RESTORATION,

            # mps
            # wow_data.PALADIN_RETRIBUTION,
            # wow_data.DEATHKNIGHT_UNHOLY,
            # wow_data.DEMONHUNTER_HAVOC,
            # wow_data.SHAMAN_ENHANCEMENT,

            # rdps
            # wow_data.SHAMAN_ELEMENTAL,
            wow_data.MONK_WINDWALKER,
            # wow_data.HUNTER_BEASTMASTERY,
            # wow_data.HUNTER_MARKSMANSHIP,
            # wow_data.MAGE_FIRE,
            # wow_data.WARLOCK_AFFLICTION,
            # wow_data.WARLOCK_DESTRUCTION,
        ]

    tasks = []
    for spec in specs:
        for boss in bosses:
            f = generate_ranking_report(boss, spec)
            tasks += [asyncio.create_task(f)]

    # if DEBUG:
    #     n = 1
    #     tasks, tasks_cancel = tasks[:n], tasks[n:]
    #     for task in tasks_cancel:
    #         task.cancel()
    await asyncio.gather(*tasks)


async def _generate_reports_index(heal_comps):
    data = {}
    data["boss"] = wow_data.ENCOUNTERS[-1] # Sire
    data["heal_comps"] = heal_comps
    path = f"{OUTPUT_FOLDER}/reports_index.html"
    await render("reports_index.html", path, data)


################################
#       Comps
#


async def _generate_comp_report(comp):
    boss = wow_data.ENCOUNTERS[-1] # Sire

    search = comp.get("search")
    logger.info("[COMP REPORT] find reports: %s", comp.get("name"))
    fights = await WCL_CLIENT.find_reports(encounter=boss["id"], search=search)

    if DEBUG:
        fights = fights[:5]

    # Get Spells and avoid duplicates
    spells = {spell_id: spell for spec in comp.get("specs") for spell_id, spell in spec.all_spells.items()}
    spells = spells.values()

    extra_filter = comp.get("extra_filter")

    for fight in fights:
        logger.info("[COMP REPORT] fetch fight: %s", comp.get("name"))
        await fight.fetch(WCL_CLIENT, spells=spells, extra_filter=extra_filter)
        fight.players.sort(key=lambda p: p.spec.full_name)

    # get a list of all used spells
    used_spells = [p.spells_used for f in fights for p in f.players]
    used_spells = utils.flatten(used_spells)
    used_spells = list(set(used_spells))

    # assamble data and render
    data = {}
    data["comp"] = comp
    data["boss"] = boss
    data["fights"] = fights
    data["all_spells"] = used_spells
    path = f"{OUTPUT_FOLDER}/comps_heal_{comp['name'].lower()}.html"
    await render("report.html", path, data)


async def generate_reports():

    # for comp in wow_data.HEAL_COMPS:
    #     specs = comp.get("specs", [])
    #     name =  comp.get("name", "")
    #     print(name)

    await _generate_reports_index(wow_data.HEAL_COMPS)
    for comp in wow_data.HEAL_COMPS:
        await _generate_comp_report(comp)
        if DEBUG:
            return


################################
#       Main
#

async def main():
    try:
        # load cache
        await WCL_CLIENT.cache.load()

        # auth once
        await WCL_CLIENT.update_auth_token()

        # generate
        await render_index()
        await generate_rankings()
        await generate_reports()

    except KeyboardInterrupt:
        logger.info("closing...")

    finally:
        logger.info("SAVING Cache!")
        await WCL_CLIENT.cache.save()


if __name__ == '__main__':
    # asyncio.run(main())
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())