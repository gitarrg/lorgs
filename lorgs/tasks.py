# IMPORT STANDARD LIBRARIES
import time
import asyncio

# IMPORT THIRD PARTY LIBRARIES
# from celery import Celery
import sqlalchemy as sa


# IMPORT LOCAL LIBRARIES
from lorgs import utils
from lorgs.celery import celery
from lorgs.cache import Cache
from lorgs import db
from lorgs.logger import logger
from lorgs.models import loader
from lorgs.models import warcraftlogs_ranking
from lorgs.models.encounters import RaidBoss
from lorgs.models.specs import WowSpec


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
def load_spec_ranking(self, boss_id, spec_id, limit=50):
    self.update_state(state="STARTED")

    ##############
    # Get
    # FIXME

    boss = RaidBoss.query.options(
        sa.orm.joinedload(RaidBoss.zone),
    ).get(boss_id)

    spec = WowSpec.query.options(
        sa.orm.joinedload(WowSpec.spells),
        sa.orm.joinedload(WowSpec.wow_class),
    ).get(spec_id)
    logger.info(f"{boss.name} vs. {spec.name} {spec.wow_class.name} start")

    # TODO: merge with existing data, and only query new
    warcraftlogs_ranking.RankedCharacter.query.filter_by(spec=spec, boss=boss).delete()
    db.session.commit()

    ##############
    # run
    task = loader.load_spec_rankings(spec=spec, boss=boss, limit=limit)
    players = asyncio.run(task)
    logger.info(f"{boss.name} vs. {spec.name} {spec.wow_class.name} query done")

    ##############
    # Add to DB
    all_casts = utils.flatten(player.casts for player in players)
    db.session.bulk_save_objects(players)
    db.session.bulk_save_objects(all_casts)
    db.session.commit()
    logger.info(f"{boss.name} vs. {spec.name} {spec.wow_class.name} added to DB!")


@celery.task(bind=True, name="load_report")
def load_report(self, report_id):
    self.update_state(state="STARTED")

    report = Report(report_id=report_id)
    self.update_state(state="PROGRESS")
    asyncio.run(loader.load_report(report))

    Cache.set(f"report/{report_id}", report.as_dict())
