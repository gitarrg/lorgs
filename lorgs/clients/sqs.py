"""Client to interact with AWS SQS."""

# IMPORT STANDARD LIBRARIES
from typing import List, Dict, Any
import json
import os
import uuid

# IMPORT THIRD PARTY LIBRARIES
import boto3

# IMPORT LOCAL LIBRARIES
from lorgs import utils


# sqs = boto3.resource("sqs")
SQS_CLIENT = boto3.client("sqs")

SQS_QUEUE_URL = os.getenv("SQS_QUEUE_URL") or ""
# SQS_QUEUE = sqs.Queue(url=SQS_QUEUE_URL)


def send_message(payload, queue_url=SQS_QUEUE_URL, message_group = ""):

    message_group = message_group or str(uuid.uuid4())
    return SQS_CLIENT.send_message(
        QueueUrl=queue_url,
        MessageGroupId=message_group,
        MessageBody=json.dumps(payload),
    )


def send_message_batch(payloads: List[Dict[str, Any]], queue_url = "", chunk_size=10):
    """Batch Submit multiple Messages"""
    print("submit_messages", payloads)

    # Wrap Payloads
    messages = [{
        "Id": str(i),
        "MessageGroupId": str(uuid.uuid4()),
        "MessageBody": json.dumps(payload),
    } for i, payload in enumerate(payloads)]

    # Send
    for entries in utils.chunks(messages, n=chunk_size):
        print("entries", entries)
        SQS_CLIENT.send_message_batch(
            QueueUrl=queue_url,
            Entries=entries, # type: ignore
        )
        # print("response", response)
