"""Model to Store Task Status."""

# IMPORT THIRD PARTY LIBRARIES
import arrow
import mongoengine as me

# IMPORT LOCAL LIBRARIES
from lorgs.lib import mongoengine_arrow


class Task(me.Document):

    STATUS_NEW = "new"
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
    _status: str = me.StringField(default=STATUS_NEW, db_field ="status") # type: ignore[override]
    updated: arrow.Arrow = mongoengine_arrow.ArrowDateTimeField(default=arrow.utcnow)  # type: ignore[override]
    message: str = me.StringField(default="") # type: ignore[override]

    @classmethod
    def from_id(cls, task_id):
        task: cls = cls.objects(task_id=task_id).first()  # type: ignore
        if not task:
            task = cls(task_id=task_id)

        return task

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        self._status = value
        self.updated = arrow.utcnow()
        self.save()
