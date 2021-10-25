# IMPORT STANDARD LIBRARIES

# IMPORT THIRD PARTY LIBRARIES
import json
import quart

# IMPORT LOCAL LIBRARIES
from lorgs.logger import logger
from lorgs import utils
from lorgs.cache import cache
from lorgs.models.warcraftlogs_user_report import UserReport
from lorgs.routes.api_tasks import create_cloud_function_task
from lorgs.client import InvalidReport


blueprint = quart.Blueprint("api/user_reports", __name__)


@blueprint.route("/<string:report_id>")
@cache.cached(query_string=True)
def get_user_report(report_id):
    """Returns the overview about a user report.

    If specified Fights and Players can be included

    Query Args:
        fights[list[int], options]: list of fights to include
        players[list[int, optional]]: list of players to include

    """
    user_report = UserReport.from_report_id(report_id=report_id)
    if not user_report:
        return {"message": "not found"}
        # return "Report not found.", 404

    return user_report.as_dict()


@blueprint.route("/<string:report_id>/fights")
@cache.cached(query_string=True)
def get_fights(report_id):
    """Get Fights in a report."""
    user_report = UserReport.from_report_id(report_id=report_id)

    fight_ids = quart.request.args.get("fight", type=utils.str_int_list)
    player_ids = quart.request.args.get("player", type=utils.str_int_list)

    if not user_report:
        return "Report not found.", 404

    report = user_report.report
    fights = [fight for fight in report.fights if fight.fight_id in fight_ids]


    return {
        "fights": [fight.as_dict(player_ids=player_ids) for fight in fights]
    }


@blueprint.route("/<string:report_id>/fights/<int:fight_id>")
@cache.cached()
def get_fight(report_id, fight_id):
    """Get a single fight from a report."""
    user_report = UserReport.from_report_id(report_id=report_id)
    if not user_report:
        return "Report not found.", 404

    fight = user_report.report.get_fight(fight_id=fight_id)
    return fight.as_dict()


@blueprint.route("/<string:report_id>/fights/<int:fight_id>/players/<int:source_id>")
@cache.cached()
def get_player(report_id, fight_id, source_id):
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


@blueprint.route("/<string:report_id>/load_overview")
async def load_user_report_overview(report_id):
    """Load a Report's Overview/Masterdata."""
    refresh = quart.request.args.get("refresh", default=False, type=json.loads)

    user_report = UserReport.from_report_id(report_id=report_id, create=True)

    needs_to_load = refresh or not user_report.is_loaded
    if needs_to_load:
        try:
            await user_report.load()
        except InvalidReport:
            return "invalid report", 404
        else:
            user_report.save()

    return user_report.as_dict()


@blueprint.route("/<string:report_id>/load")
async def load_user_report(report_id):
    """Load a Report

    Args:
        report_id(str): the report to load
        fights[list(int)]: fight ids
        player[list(int)]: player ids

    """
    ################################
    # parse inputs
    # keep as str, as we just pass them trough
    fight_ids = quart.request.args.get("fight", type=str)
    player_ids = quart.request.args.get("player", type=str)

    logger.info("load: %s / fights: %s / players: %s", report_id, fight_ids, player_ids)
    if not (fight_ids and player_ids):
        return "Missing fight or player ids", 403

    ################################
    # create task
    task_id = await create_cloud_function_task(
        function_name="load_user_report",
        report_id=report_id,
        fight=fight_ids,
        player=player_ids,
    )
    return {"task_id": task_id}
