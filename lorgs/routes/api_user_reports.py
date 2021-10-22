# IMPORT STANDARD LIBRARIES

# IMPORT THIRD PARTY LIBRARIES
import flask

# IMPORT LOCAL LIBRARIES
from lorgs.logger import logger
from lorgs.cache import cache
from lorgs.models.warcraftlogs_user_report import UserReport


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
        return "Report not found.", 404

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

@blueprint.route("/load/<string:report_id>")
async def load_user_report(report_id):
    """Load a Report

    Args:
        report_id(str): the report to load
        fights[list(int)]: fight ids
        player[list(int)]: player ids

    """
    # parse inputs
    fight_ids = flask.request.args.getlist("fight", type=int)
    player_ids = flask.request.args.getlist("player", type=int)
    logger.info("load: %s / fights: %s / players: %s", report_id, fight_ids, player_ids)
    if not (fight_ids and player_ids):
        return "Missing fight or player ids", 403

    # loading...
    user_report = UserReport.from_report_id(report_id=report_id, create=True)
    await user_report.load_fights(fight_ids=fight_ids, player_ids=player_ids)
    user_report.save()

    # return
    return "done"
