"""Setup our Celery Instance."""
# IMPORT STANDARD LIBRARIES
import os

# IMPORT THIRD PARTY LIBRARIES
import celery as celery_

# IMPORT LOCAL LIBRARIES
from lorgs import db


# make sure these are set
CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL") or os.getenv("REDISCLOUD_URL") or os.getenv("REDIS_URL") or "redis://localhost:6379"
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND") or CELERY_BROKER_URL


class CeleryTask(celery_.Task):
    """Custom TaskClass to ensure we close our database sessions when the tasks ends."""

    def after_return(self, *args, **kwargs):
        """Remove and DB Sessions."""
        db.session.remove()
        return super().after_return(*args, **kwargs)


celery = celery_.Celery(  # pylint: disable=invalid-name
    "lorgs_celery",
    broker=CELERY_BROKER_URL,
    backend=CELERY_RESULT_BACKEND,
    task_cls=CeleryTask,
    include=["lorgs.tasks"]
)
