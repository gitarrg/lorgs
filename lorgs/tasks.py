# IMPORT STANDARD LIBRARIES
import time
import asyncio

# IMPORT THIRD PARTY LIBRARIES
# from celery import Celery

# IMPORT LOCAL LIBRARIES
from lorgs.celery import celery
from lorgs import db
from lorgs import data
from lorgs.logger import logger
# from lorgs.models import loader
from lorgs.models import warcraftlogs_ranking
# from lorgs.models.encounters import RaidBoss
# from lorgs.models.specs import WowSpec
# from lorgs.models.warcraftlogs_report import Report


raise ValueError("Deprecated")


@celery.task(bind=True, name="debug_task")
def debug_task(self):
    task_info = {"name": "DebugTask"}
    for i in range(10):
        logger.info("Step: %d", i)
        time.sleep(0.25)
        task_info["step"] = i
        self.update_state(state="PROGRESS", meta=task_info)

    # import datetime
    # x = datetime.datetime.now()
    # Cache.set("test_value", str(x))
    # print("running", *args, **kwargs)
    task_info["players"] = ["A", "B", "C"]
    return task_info


@celery.task(bind=True, name="load_spec_ranking")
def load_spec_ranking(self, boss_slug, spec_slug, limit=50):
    # self.update_state(state="STARTED")

    ##############
    # Get
    ranking = warcraftlogs_ranking.SpecRanking.get_or_create(boss_slug=boss_slug, spec_slug=spec_slug)

    ##############
    # run
    task = ranking.load(limit=limit)
    asyncio.run(task)

    logger.info(f"{ranking.boss.name} vs. {ranking.spec.name} {ranking.spec.wow_class.name} query done")

    ##############
    # Save

    print("!!!!! ranking", len(ranking.reports))

    ranking.save()

    # db.session.bulk_save_objects(all_casts)
    logger.info(f"{ranking.boss.name} vs. {ranking.spec.name} {ranking.spec.wow_class.name} saved to DB!")


@celery.task(bind=True, name="load_report")
def load_report(self, report_id):
    self.update_state(state="STARTED")

    # get report
    report = Report.query.get(report_id) or Report(report_id=report_id)

    # load report
    self.update_state(state="PROGRESS")
    asyncio.run(report.load())

    # save to DB
    db.session.add(report)
    db.session.commit()

    self.update_state(state="DONE")
