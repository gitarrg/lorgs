#!/usr/bin/env python
"""Load a some test reports. Useful to assist in development."""

import asyncio

import dotenv
dotenv.load_dotenv() # pylint: disable=wrong-import-position

from lorgs import data
from lorgs import db
# from lorgs.models import warcraftlogs_ranking
# from lorgs.models import warcraftlogs_comps
from lorgs.models import specs

import shutil
import subprocess


########################################
#
#


def resize_image():


def resize_images():



async def copy_source_images():

    src_root = "/mnt/d/dev/lorgs_extra/wow-ui-textures/ICONS"
    tar_root = "/mnt/d/dev/lorgs/lorgs/static/images/spells/src"

    spells = specs.WowSpell.all


    for spell in spells:
        print(spell.icon)

        icon_name = spell.icon.split(".")[0]

        src_path = f"{src_root}/{icon_name}.PNG"
        tar_path = f"{tar_root}/{icon_name}.PNG"

        try:
            shutil.copy2(src_path, tar_path)
        except FileNotFoundError:
            print("file not found:", src_path)





async def main():
    await copy_source_images()


if __name__ == '__main__':
    asyncio.run(main())
