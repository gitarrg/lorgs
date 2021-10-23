# IMPORT STANDARD LIBRARIES

# IMPORT THIRD PARTY LIBRARIES
import json
import flask

# IMPORT LOCAL LIBRARIES
from lorgs.logger import logger
from lorgs.cache import cache
from lorgs.models.warcraftlogs_user_report import UserReport
from lorgs.routes.api_tasks import create_cloud_function_task
from lorgs.client import InvalidReport


blueprint = flask.Blueprint("api.user_reports", __name__)


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
    user_report = UserReport.from_report_id(report_id=report_id, create=True)

    try:
        await user_report.load()
    except InvalidReport:
        return flask.make_response("invalid report", 404)
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
    fight_ids = flask.request.args.getlist("fight", type=int)
    player_ids = flask.request.args.getlist("player", type=int)
    direct = flask.request.args.get("direct", default=False, type=json.loads)

    logger.info("load: %s / fights: %s / players: %s", report_id, fight_ids, player_ids)
    if not (fight_ids and player_ids):
        return "Missing fight or player ids", 403

    ################################
    # loading...
    if direct:
        user_report = UserReport.from_report_id(report_id=report_id, create=True)
        await user_report.load_fights(fight_ids=fight_ids, player_ids=player_ids)
        user_report.save()
        return "done"

    ################################
    # create task
    task_id = create_cloud_function_task("user_report_load")
    return {"task_id": task_id}
