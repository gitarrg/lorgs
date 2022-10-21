"""Model to Store Task Status."""

# IMPORT STANDARD LIBRARIES
import json
import typing
import os

# IMPORT THIRD PARTY LIBRARIES
import arrow
import boto3
import mongoengine as me

# IMPORT LOCAL LIBRARIES
from lorgs.lib import mongoengine_arrow


# SQS_CLIENT = boto3.client("sqs")
SQS_QUEUE_URL = os.getenv("SQS_QUEUE_URL") or ""
sqs = boto3.resource("sqs")


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

    task_id: str = me.StringField(primary_key=True)
    _status: str = me.StringField(default=STATUS_NEW, db_field ="status")
    updated: arrow.Arrow = mongoengine_arrow.ArrowDateTimeField(default=arrow.utcnow)


    @classmethod
    def from_id(cls, task_id):
        task: cls = cls.objects(task_id=task_id).first()  # pylint: disable=no-member
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

    @classmethod
    def submit(cls, task_type: str, payload: typing.Dict):

        queue = sqs.Queue(url=SQS_QUEUE_URL)

        message = queue.send_message(
            MessageBody=json.dumps(payload),
            MessageGroupId=task_type,
            MessageAttributes={
                "task": { "DataType": "String", "StringValue": task_type },
            }
        )
        message_id = message.get("MessageId")


        task = cls(task_id=message_id)
        task.save()
        return task
