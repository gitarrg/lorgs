"""Model to Store Task Status."""

# IMPORT STANDARD LIBRARIES
import datetime
import typing

# IMPORT LOCAL LIBRARIES
from lorgs.models.base import redis


class Task(redis.RedisModel):
    """"""

    class STATUS:
        NEW = "new"
        WAITING = "waiting"
        IN_PROGRESS = "in-progress"
        DONE = "done"
        FAILED = "failed"

    task_id: str
    status: str = STATUS.NEW
    updated: datetime.datetime = datetime.datetime.now()
    message: str = ""
    items: dict[str, typing.Any] = {}

    # Config

    key: typing.ClassVar[str] = "{table_name}:{task_id}"
    # expire time for the tasks (1 hour)
    ttl: typing.ClassVar[int] = 60 * 60
