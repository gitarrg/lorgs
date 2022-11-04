"""Handler to Load User Reports.

to be triggered via SQS

"""
# IMPORT STANDARD LIBRARIES
import json
import typing

# IMPORT LOCAL LIBRARIES
from lorgs import data # pylint: disable=unused-import
from lorgs import db
from lorgs import events
from lorgs.models.task import Task
from lorgs.models.warcraftlogs_user_report import UserReport

if typing.TYPE_CHECKING:
    from lorgs.models import warcraftlogs_actor


def set_task_item_status(task: Task, status: str):
    """Create a Callback to update an Item in Task to the given Status."""

    async def setter(event: events.Event) -> None:
        actor: typing.Optional["warcraftlogs_actor.BaseActor"] = event.payload.get("actor")
        if not actor:
            return

        fight_id = actor.fight.fight_id if actor.fight else 0
        source_id = actor.source_id
        if (fight_id <= 0) or (source_id <= 0):
            return

        task.set(**{f"items.{fight_id}_{source_id}.status": status})

    return setter


async def load_user_report(
    report_id: str,
    fight_ids: typing.List[int] = [],
    player_ids: typing.List[int] = [],
    **kwargs
) -> None:
    print(f"[load_user_report] report_id={report_id} fight_ids={fight_ids} player_ids={player_ids}")
    if not (report_id and fight_ids and player_ids):
        raise ValueError("Missing fight or player ids")

    ################################
    # loading...
    user_report = UserReport.from_report_id(report_id=report_id, create=True)
    await user_report.report.load_fights(fight_ids=fight_ids, player_ids=player_ids)
    user_report.save()


async def main(message):

    # Task Status Updates
    message_id = message.get("messageId")

    task = Task.get(key=message_id, create=True)
    task.set(status=task.STATUS.IN_PROGRESS)
    events.register("actor.load.start", set_task_item_status(task, task.STATUS.IN_PROGRESS))
    events.register("actor.load.done", set_task_item_status(task, task.STATUS.DONE))
    events.register("actor.load.failed", set_task_item_status(task, task.STATUS.FAILED))

    ###########################
    # Main
    message_body = message.get("body")
    message_payload = json.loads(message_body)

    try:
        await load_user_report(**message_payload)
    except:
        task.set(status=task.STATUS.FAILED)
    else:
        task.set(status=task.STATUS.DONE)

