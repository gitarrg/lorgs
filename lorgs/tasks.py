
# IMPORT STANDARD LIBRARIES
import os
import time
import asyncio

# IMPORT THIRD PARTY LIBRARIES
from celery import Celery

# IMPORT LOCAL LIBRARIES
from lorgs import data
from lorgs.cache import Cache
from lorgs.logger import logger
from lorgs.models import loader
from lorgs.models.encounters import RaidBoss
from lorgs.models.reports import Report
from lorgs.models.reports import SpecRanking
from lorgs.models.specs import WowSpec



# make sure these are set
os.environ["CELERY_BROKER_URL"] = os.getenv("CELERY_BROKER_URL") or os.getenv("REDISCLOUD_URL") or os.getenv("REDIS_URL") or "redis://localhost:6379"
os.environ["CELERY_RESULT_BACKEND"] = os.getenv("CELERY_RESULT_BACKEND") or os.environ["CELERY_BROKER_URL"]


logger.info("CELERY_BROKER_URL: %s", os.environ["CELERY_BROKER_URL"])
celery = Celery("lorgs_celery")


@celery.task(bind=True, name="debug_task")
def debug_task(self):
    task_info = {"name": "DebugTask"}
    for i in range(10):
        time.sleep(1)
        task_info["step"] = i
        self.update_state(state="PROGRESS", meta=task_info)

    # import datetime
    # x = datetime.datetime.now()
    # Cache.set("test_value", str(x))
    # print("running", *args, **kwargs)
    task_info["players"] = ["A", "B", "C"]
    return task_info


@celery.task(name="load_spell_icons")
def load_spell_icons():
    spells = data.SPELLS
    logger.info("%d spells", len(spells))

    spell_infos = asyncio.run(loader.load_spell_icons(spells))

    # save cache
    spell_infos = [info for info in spell_infos.values()]
    Cache.set("spell_infos", spell_infos)


@celery.task(bind=True, name="load_spec_ranking")
def load_spec_ranking(self, boss_id, spec_full_name_slug, limit=50):
    self.update_state(state="STARTED")

    # Get
    spec = WowSpec.get(full_name_slug=spec_full_name_slug)
    boss = RaidBoss.get(id=boss_id)
    logger.info(f"{boss.name} vs. {spec.name} {spec.wow_class.name} start")

    # run
    spec_ranking = SpecRanking(spec, boss)
    asyncio.run(spec_ranking.update(limit=limit))

    logger.info(f"{boss.name} vs. {spec.name} {spec.wow_class.name} done")


@celery.task(bind=True, name="load_report")
def load_report(self, report_id):
    self.update_state(state="STARTED")

    report = Report(report_id=report_id)
    self.update_state(state="PROGRESS")
    asyncio.run(loader.load_report(report))

    Cache.set(f"report/{report_id}", report.as_dict())
