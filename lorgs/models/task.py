"""Model to store Task Status.

Somehow its incredibly difficult or even impossible to access completed
tasks on Google Cloud Tasks... so we need some additional logic to keep
track of tasks
"""

# IMPORT STANDARD LIBRARIES
import uuid

# IMPORT THIRD PARTY LIBRARIES
import arrow
import mongoengine as me

# IMPORT LOCAL LIBRARIES
from lorgs.lib import mongoengine_arrow


# expire time for the tasks (1 week)
TTL = 60 * 60 * 24 * 7


class Task(me.Document):

    STATUS_NEW = "new"  # just created. most likely not even dispatched to the queue yet
    STATUS_PENDING = "pending" # task has been submitted but not started yet
    STATUS_IN_PROGRESS = "in_progress" # task is currently beeing executed
    STATUS_DONE = "done"
    STATUS_FAILED = "failed"

    id: str = me.UUIDField(default=uuid.uuid4, binary=False, primary_key=True)

    # time the task was created
    created: arrow.Arrow = mongoengine_arrow.ArrowDateTimeField(default=arrow.utcnow)

    # time the task has last been changed (eg.: started/complted/failed)
    updated: arrow.Arrow = mongoengine_arrow.ArrowDateTimeField(default=arrow.utcnow)

    # current status of the task
    _status = me.StringField(default=STATUS_NEW, db_field="status")

    # task payload, used to store any additional data
    payload = me.DictField()

    meta = {
        'indexes': [
            {'fields': ['updated'], 'expireAfterSeconds': TTL}
        ]
    }


    def __repr__(self):
        return f"Task({self.id}, status={self.status}, updated={self.updated})"

    def as_dict(self):
        return {
            "id": self.id,
            "status": self.status,
            "crated": self.created.timestamp(),
            "updated": self.updated.timestamp(),
        }

    @property
    def status(self):
        """Current status of the task.

        Changing this value also updates the "updated"-timestamp
        """
        return self._status

    @status.setter
    def status(self, status):
        self._status = status
        self.updated = arrow.utcnow()
