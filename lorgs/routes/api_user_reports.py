# IMPORT THIRD PARTY LIBRARIES
import fastapi
from fastapi.routing import run_endpoint_function
from fastapi_cache.decorator import cache

# IMPORT LOCAL LIBRARIES
from lorgs import utils
from lorgs.client import InvalidReport
from lorgs.logger import logger
from lorgs.models.warcraftlogs_user_report import UserReport
from lorgs.routes.api_tasks import create_cloud_function_task


router = fastapi.APIRouter()


@router.get("/{report_id}")
@cache()
async def get_user_report(report_id):
    """Returns the overview about a user report."""
    user_report = UserReport.from_report_id(report_id=report_id)
    if not user_report:
        return {"message": "not found"}
        # return "Report not found.", 404

    return user_report.as_dict()


@router.get("/{report_id}/fights")
@cache()
async def get_fights(report_id, fight: str, player: str):
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
    fights = [fight for fight in report.fights if fight.fight_id in fight_ids]
    return {
        "fights": [fight.as_dict(player_ids=player_ids) for fight in fights]
    }


@router.get("/{report_id}/fights/{fight_id}")
@cache()
async def get_fight(report_id: str, fight_id: int):
    """Get a single fight from a report."""
    user_report = UserReport.from_report_id(report_id=report_id)
    if not user_report:
        return "Report not found.", 404

    fight = user_report.report.get_fight(fight_id=fight_id)
    return fight.as_dict()


@router.get("/{report_id}/fights/{fight_id}/players/{source_id}")
@cache()
async def get_player(report_id: str, fight_id: int, source_id: int):
    """Get a single player from a fight."""
    user_report = UserReport.from_report_id(report_id=report_id)
    if not user_report:
        return "Report not found.", 404

    fight = user_report.report.get_fight(fight_id=fight_id)
    if not fight:
        return "Invalid Fight ID", 404

    player = fight.get_player(source_id=source_id)
    if not player:
        return "Invalid Source ID", 404

    return player.as_dict()


################################################################################


@router.get("/{report_id}/load_overview")
async def load_user_report_overview(report_id: str, refresh=False):
    """Load a Report's Overview/Masterdata."""
    user_report = UserReport.from_report_id(report_id=report_id, create=True)
    if not user_report:
        return "Report not found.", 404

    needs_to_load = refresh or not user_report.is_loaded
    if needs_to_load:
        try:
            await user_report.load()
        except InvalidReport:
            return "invalid report", 404
        else:
            user_report.save()

    return user_report.as_dict()


@router.get("/{report_id}/load")
async def load_user_report(report_id: str, fight: str, player: str):
    """Load a Report

    Args:
        report_id(str): the report to load
        fight (str): dot separeted list of fight ids (eg.: 2.4.15)
        player (str): dot separeted list of player ids (eg.: 1.5.20)

    """
    # Note:
    #   fight and player-inputs are kept as str,
    #   as we just pass them trough
    task_id = await create_cloud_function_task(
        function_name="load_user_report",
        report_id=report_id,
        fight=fight,
        player=player,
    )
    return {"task_id": task_id}
