"""Model to Store Task Status."""

# IMPORT STANDARD LIBRARIES
import typing
import datetime

# IMPORT LOCAL LIBRARIES
from lorgs.clients import redis_store


class Task(redis_store.RedisModel):
    """"""

    class STATUS:
        NEW = "new"
        WAITING = "waiting"
        IN_PROGRESS = "in-progress"
        DONE = "done"
        FAILED = "failed"

    # expire time for the tasks (1 hour)
    ttl = 60 * 60

    status: str = STATUS.NEW
    updated: datetime.datetime = datetime.datetime.now()
    message: str = ""
    items: dict[str, typing.Any] = {}
