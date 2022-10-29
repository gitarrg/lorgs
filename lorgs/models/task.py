"""Model to Store Task Status."""

# IMPORT THIRD PARTY LIBRARIES
from typing import Optional
import arrow
import mongoengine as me

# IMPORT LOCAL LIBRARIES
from lorgs.lib import mongoengine_arrow


class Task(me.Document):

    STATUS_NEW = "new"
    STATUS_WAITING = "waiting"
    STATUS_IN_PROGRESS = "in-progress"
    STATUS_DONE = "done"
    STATUS_FAILED = "failed"

    # expire time for the tasks (1 week)
    TTL = 60 * 60 * 24 * 7

    meta = {
        # ignore non existing properties
        "strict": False,

        'indexes': [
            {'fields': ['updated'], 'expireAfterSeconds': TTL}
        ]
    }

    task_id: str = me.StringField(primary_key=True) # type: ignore[override]
    status: str = me.StringField(default=STATUS_NEW) # type: ignore[override]
    updated: arrow.Arrow = mongoengine_arrow.ArrowDateTimeField(default=arrow.utcnow)  # type: ignore[override]
    message: str = me.StringField(default="") # type: ignore[override]

    @classmethod
    def from_id(cls, task_id) -> Optional["Task"]:
        return cls.objects(task_id=task_id).first()  # type: ignore

    @classmethod
    def update_task(cls, task_id: str, **kwargs):

        task = cls.from_id(task_id)
        if not task:
            return

        updated = False

        if "message" in kwargs:
            task.message = kwargs["message"]
            updated = True
        if "status" in kwargs:
            task.status = kwargs["status"]
            updated = True

        if updated:
            task.updated = arrow.utcnow()
            task.save()
