"""Client to interact with AWS SQS."""

# IMPORT STANDARD LIBRARIES
import json
import os
import uuid
from typing import Any, Dict, List

# IMPORT THIRD PARTY LIBRARIES
import boto3

# IMPORT LOCAL LIBRARIES
from lorgs import utils


SQS_CLIENT = boto3.client("sqs")
SQS_QUEUE_URL = os.getenv("SQS_QUEUE_URL") or ""


def send_message(payload: Any, queue_url="", message_group=""):
    """Send a single Message."""
    message_group = message_group or str(uuid.uuid4())
    return SQS_CLIENT.send_message(
        QueueUrl=queue_url or SQS_QUEUE_URL,
        MessageGroupId=message_group,
        MessageBody=json.dumps(payload),
    )


def send_message_batch(payloads: List[Dict[str, Any]], queue_url="", chunk_size=10):
    """Batch Submit multiple Messages."""

    # Wrap Payloads
    messages = [
        {
            "Id": str(i),
            "MessageGroupId": str(uuid.uuid4()),
            "MessageBody": json.dumps(payload),
        }
        for i, payload in enumerate(payloads)
    ]

    # Send
    for entries in utils.chunks(messages, n=chunk_size):
        SQS_CLIENT.send_message_batch(
            QueueUrl=queue_url or SQS_QUEUE_URL,
            Entries=entries,  # type: ignore
        )
