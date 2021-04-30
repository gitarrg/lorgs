
# pylint: disable=wrong-import-position,invalid-name
import asyncio

import dotenv
dotenv.load_dotenv()

from lorgs import data
from lorgs import utils
from lorgs.models.specs import WowRole
from lorgs.models.specs import WowClass
from lorgs.models.specs import WowSpell
from lorgs.models.specs import WowSpec
from lorgs.models import Report
from lorgs.cache import Cache
from lorgs.models import loader

from lorgs.app import create_app

app = create_app()

from pprint import pprint


import redis
client = redis.Redis(host="localhost")#, port=6379, password="mypassword")
import json


async def test_1():
    """Load a report."""

    report_id = "6YGnLdrtyKMWwcmx"

    """
    report = Report(report_id=report_id)
    await loader.load_report(report)
    report = Cache.set(f"report/{report_id}", report, timeout=0)
    """

    report = Cache.get(f"report/{report_id}")
    report.fights = report.fights[:3]
    pprint(report.as_dict())

    client.set("test", json.dumps(report.as_dict()))

    # report = Cache.set(f"report/{report_id}")

async def test_2():


    import pickle
    spec = WowSpec.get(full_name_slug="paladin-holy")
    spec = pickle.loads(pickle.dumps(spec))
    pprint(spec.as_dict())

    # res.file.read()  # OK




async def main():
    await test_1()
    # await test_2()


if __name__ == '__main__':
    asyncio.run(main())





"""
Cache.set("spell_infos", {}, timeout=600)

# import pickle
wow_class = WowSpec.get(wow_class__name="Druid", name="Restoration")
spells = wow_class.spells

data = spells[:3]
Cache.set("test", data)

print("======== SAVED ========")

data = Cache.get("test")
print(data)

# with app.app_context():
"""
