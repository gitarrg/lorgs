"""Routes related to UserReports."""
# IMPORT STANDARD LIBRARIES
import itertools

# IMPORT THIRD PARTY LIBRARIES
import fastapi

# IMPORT LOCAL LIBRARIES
from lorgs import utils
from lorgs.clients.wcl import InvalidReport
from lorgs.clients import sqs
from lorgs.models.task import Task
from lorgs.models.warcraftlogs_user_report import UserReport


router = fastapi.APIRouter()


@router.get("/{report_id}")
async def get_user_report(report_id: str):
    """Returns the overview about a user report."""
    user_report = UserReport.from_report_id(report_id=report_id)
    if not user_report:
        return {"message": "not found"}

    return user_report.as_dict()


@router.get("/{report_id}/fights")
async def get_fights(report_id: str, fight: str, player: str = ""):
    """Get Fights in a report.

    Args:
        report_id: id of the report to load (code/id from the warcraftlogs url)
        fight (str): dot separeted list of fight ids (eg.: 2.4.15)
        player (str): dot separeted list of player ids (eg.: 1.5.20)

    """
    user_report = UserReport.from_report_id(report_id=report_id)
    if not user_report:
        return "Report not found.", 404

    fight_ids = utils.str_int_list(fight)
    player_ids = utils.str_int_list(player)

    report = user_report.report
    fights = report.get_fights(*fight_ids)
    return {
        "fights": [fight.as_dict(player_ids=player_ids) for fight in fights]
    }


################################################################################


@router.get("/{report_id}/load_overview")
async def load_user_report_overview(response: fastapi.Response, report_id: str, refresh: bool = False):
    """Load a Report's Overview/Masterdata."""
    user_report = UserReport.from_report_id(report_id=report_id, create=True)
    if not user_report:
        return "Report not found.", 404

    needs_to_load = refresh or not user_report.is_loaded
    if needs_to_load:
        try:
            await user_report.report.load_summary()
        except InvalidReport:
            return {"error": "Invalid URL."}
        except PermissionError:
            return {"error": "No permission to view this report."}
        else:
            user_report.save()

    response.headers["Cache-Control"] = "no-cache"
    return user_report.as_dict()


@router.get("/{report_id}/load")
async def load_user_report(response: fastapi.Response, report_id: str, fight: str, player: str, user_id: int = 0):
    """Load a Report

    Args:
        report_id(str): the report to load
        fight (str): dot separeted list of fight ids (eg.: 2.4.15)
        player (str): dot separeted list of player ids (eg.: 1.5.20)
        user_id (int, optional): user id to identify logged in users

    """
    response.headers["Cache-Control"] = "no-cache"

    fight_ids = utils.str_int_list(fight)
    player_ids = utils.str_int_list(player)

    payload = {
        "task": "load_user_report",
        "report_id": report_id,
        "user_id": user_id,
        "fight_ids": utils.str_int_list(fight),
        "player_ids": utils.str_int_list(player),
    }

    message = sqs.send_message(payload=payload)
    message_id = message["MessageId"]

    # task object to help track the progress
    task = Task(key=message_id, status=Task.STATUS.WAITING)

    # Add subitems to track the status more granual
    for (f, p) in itertools.product(fight_ids, player_ids):
        task.items[f"{f}.{p}"] = {"fight": f, "player": p, "status": task.status}

    task.save()

    return {
        "task_id": task.key,
        "queue": "aws",
    }
