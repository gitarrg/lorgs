#!/usr/bin/env python
"""Util to fill in some missing data."""

import asyncio
import os

import arrow
import mongoengine as me
import mongoengine_arrow


import dotenv
dotenv.load_dotenv() # pylint: disable=wrong-import-position
# os.environ["MONGO_URI"] = os.getenv("MONGO_URI_PROD") # pylint: disable=wrong-import-position

from lorgs import data
from lorgs import db
# from lorgs.models import warcraftlogs_ranking

########################################
#
#
class OldFight(me.EmbeddedDocument):
    start_time: arrow.Arrow = mongoengine_arrow.ArrowDateTimeField()
    end_time: arrow.Arrow = mongoengine_arrow.ArrowDateTimeField()

    duration = me.IntField(default=0)

    meta = {
        "strict": False # ignore non existing properties
    }

class OldReport(me.EmbeddedDocument):

    report_id = me.StringField(primary_key=True)
    start_time: arrow.Arrow = mongoengine_arrow.ArrowDateTimeField()
    fights = me.ListField(me.EmbeddedDocumentField(OldFight))

    meta = {
        "strict": False # ignore non existing properties
    }


class OldSpecRanking(me.Document):

    reports = me.ListField(me.EmbeddedDocumentField(OldReport))

    boss_slug = me.StringField()
    spec_slug = me.StringField()

    meta = {
        "collection": "spec_ranking",   # <-- read the actual reports
        "strict": False # ignore non existing properties
    }




async def load_one_spec_ranking(boss, spec, limit=5):

    print("loading", boss, "vs", spec)
    old_rankings = OldSpecRanking.objects(boss_slug=boss.full_name_slug, spec_slug=spec.full_name_slug).first()

    # loop over old reports, try to match the keys and set the new ids
    for report in old_rankings.reports:
        report.start_time = report.start_time.shift(microseconds=1)  # simply resave
        for fight in report.fights:

            if fight.duration > 1000:
                print("fight already converted")
                continue

            fight.start_time = report.start_time.shift(seconds=fight.start_time.timestamp/1000)
            end_time = report.start_time.shift(seconds=fight.end_time.timestamp/1000)

            # d = end_time - fight.start_time
            fight.duration = (end_time.timestamp - fight.start_time.timestamp) * 1000

            print("\tF: s", fight.start_time, "-", end_time, fight.duration)
            # print("\tF: e", fight.end_time)
            # print("\tF: d", fight.duration)


    # await ranking.load(limit=limit, clear_old=True)
    old_rankings.save()

async def load_spec_ranking():
    ########################################
    # Vars
    limit = 60
    bosses = data.SANCTUM_OF_DOMINATION.bosses[1:]
    specs = data.SPECS
        
    for boss in bosses:
        # tasks = []
        for spec in specs:
            await load_one_spec_ranking(boss, spec, limit=limit)
        # await asyncio.gather(*tasks)


async def main():
    await load_one_spec_ranking(data.PAINSMITH, data.DEATHKNIGHT_FROST)
    # await load_spec_ranking()
    # await remove_invalid()
    print("done")
    


if __name__ == '__main__':
    asyncio.run(main())
