
import asyncio

from lorrgs_sqs_handler.task_handlers import TASK_HANDLERS


async def process_message(message):

    attributes = message.get("messageAttributes") or {}
    message_task = attributes.get("task") or "unknown"

    message_handler = TASK_HANDLERS.get(message_task)
    if message_handler:
        await message_handler(message)


async def process_messages(messages):

    for message in messages:
        await process_message(message)


def handler(event, context):

    records = event.get("Records") or []
    if not records:
        return

    loop = asyncio.get_event_loop()
    loop.run_until_complete(process_messages(records))
    return "ok"

