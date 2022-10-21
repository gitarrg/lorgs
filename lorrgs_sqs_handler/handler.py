
import asyncio

from lorgs.models.task import Task   # pylint: disable=unused-import
from lorrgs_sqs_handler.task_handlers import load_user_report
from lorrgs_sqs_handler.task_handlers import send_discord_message


TASK_HANDLERS = {
    # for debugging
    "unknown": send_discord_message.main,

    "load_user_report": load_user_report.main,
}


async def process_message(message):

    attributes = message.get("messageAttributes") or {}
    message_task = attributes.get("task") or {}
    message_task = message_task.get("stringValue") or "unknown"

    # Task Status Updates
    message_id = message.get("messageId")
    task = Task.from_id(message_id)
    task.status = Task.STATUS_IN_PROGRESS

    # run the Handler
    message_handler = TASK_HANDLERS.get(message_task)
    if message_handler:
        await message_handler(message)

    # Task Status Updates
    task.status = Task.STATUS_DONE


async def process_messages(messages):
    """Wrapper to process all messages in the batch."""
    for message in messages:
        await process_message(message)


def handler(event, context):
    """Main Handler called by Lambda."""
    records = event.get("Records") or []
    if not records:
        return

    loop = asyncio.get_event_loop()
    loop.run_until_complete(process_messages(records))
    return "ok"

