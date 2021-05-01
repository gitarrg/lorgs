
import os
import time
import asyncio
import random

from celery import Celery

# from lorgs.app import create_app
from lorgs.cache import Cache
from lorgs.logger import logger
from lorgs.models import loader
from lorgs.models import Report
from lorgs.models.encounters import RaidBoss
from lorgs.models.reports import Report
from lorgs.models.reports import SpecRanking
from lorgs.models.specs import WowSpec


CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379")
CELERY_RESULT_BACKEND = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379")


celery = Celery(
    __name__,
    broker=CELERY_BROKER_URL,
    backend=CELERY_RESULT_BACKEND,
)


@celery.task(name="load_spell_icons")
def load_spell_icons():
    pass



@celery.task(name="load_spec_ranking")
def load_spec_ranking(boss_id, spec_full_name_slug, limit=50):

    # Get
    spec = WowSpec.get(full_name_slug=spec_full_name_slug)
    boss = RaidBoss.get(id=boss_id)
    logger.info(f"{boss.name} vs. {spec.name} {spec.wow_class.name} start")
    spec_ranking = SpecRanking(spec, boss)
    # run
    asyncio.run(spec_ranking.update(limit=limit))

    logger.info(f"{boss.name} vs. {spec.name} {spec.wow_class.name} done")



@celery.task(name="load_report")
def load_report(report_id):

    print("load_report", report_id)
    report = Report(report_id=report_id)

    print("OK pre sleep")
    asyncio.run(loader.load_report(report))
    print("done?")

    Cache.set(f"report/{report_id}", report.as_dict())
