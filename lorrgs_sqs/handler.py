# IMPORT STANDARD LIBRARIES
import asyncio
import json
import os
import typing

import boto3

# IMPORT LOCAL LIBRARIES
from lorgs import utils
from lorrgs_sqs import helpers
from lorrgs_sqs.task_handlers import load_spec_rankings
from lorrgs_sqs.task_handlers import load_user_report
from lorrgs_sqs.task_handlers import send_discord_message


TASK_HANDLERS = {
    # for debugging
    "unknown": send_discord_message.main,
    "discord": send_discord_message.main,

    "load_user_report": load_user_report.main,
    "load_spec_rankings": load_spec_rankings.main,
}


SQS_CLIENT = boto3.client("sqs")


def submit_messages(queue_url, messages, chunk_size=10):
    """"""
    print("submit_messages", messages)

    # Inject IDs
    messages = [{"Id": str(i), **msg} for i, msg in enumerate(messages)]

    for entries in utils.chunks(messages, n=chunk_size):
        print("entries", entries)
        response = SQS_CLIENT.send_message_batch(
            QueueUrl=queue_url,
            Entries=entries,
        )
        print("response", response)


async def process_message(message):

    # Task Status Updates
    # message_id = message.get("messageId")
    # task = Task.from_id(message_id)
    # task.status = Task.STATUS_IN_PROGRESS

    payload = json.loads(message.get("body") or "")
    task = payload.get("task") or "unknown"

    #################################
    # See if the message expands into multiple tasks
    # if so: resubmit those back to the queue
    # print("process_message.payload", message_payload)
    payloads = helpers.expand_keywords(payload)
    # print("process_message.payloads", payloads)
    if len(payloads) > 1:
        attributes = message.get("attributes")
        source_arn = message.get("eventSourceARN")
        queue_url = helpers.queue_arn_to_url(source_arn)

        messages = [{
            "MessageBody": json.dumps(payload),
            "MessageGroupId": attributes.get("MessageGroupId") or "undefined"
        } for payload in payloads]

        return submit_messages(queue_url, messages)

    # run the Handler
    handler = TASK_HANDLERS.get(task) or TASK_HANDLERS["unknown"]
    await handler(message)

    # Task Status Updates
    # task.status = Task.STATUS_DONE


async def process_messages(messages: typing.List):
    """Wrapper to process all messages in the batch."""
    for message in messages:
        await process_message(message)

    return {
        # TODO: track failed tasks and return IDs here
        "batchItemFailures" : []
    }


def handler(event, context=None):
    """Main Handler called by Lambda."""
    print("handler", event)
    records = event.get("Records") or []
    return asyncio.run(process_messages(records))
