# pylint: disable=wrong-import-position,invalid-name

# IMPORT STANDARD LIBRARIES
import os
import asyncio

# IMPORT THIRD PARTY LIBRARIES
import dotenv
dotenv.load_dotenv()

os.environ["DEBUG"] = "1"

from lorgs.app import create_app
from lorgs.cache import Cache
from lorgs.client import WarcraftlogsClient
from lorgs.models import loader
from lorgs.models import Report
from lorgs.models import RaidBoss
from lorgs.models import WowClass
from lorgs.models import WowSpec


# create app instance
app = create_app()
app.app_context().push()
import pprint


WCL_CLIENT = WarcraftlogsClient.get_instance()



async def test_load_report():


    report_id = "yHQTNpvtkVjw82ca" # AM Sunday
    report = Report(report_id=report_id)

    await loader.load_report(report)
    print(20 * "\n########################")

    report.fights = report.fights[:2]

    pprint.pprint(report.as_dict())



if __name__ == '__main__':
    asyncio.run(test_load_report())
