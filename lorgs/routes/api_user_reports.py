# IMPORT STANDARD LIBRARIES

# IMPORT THIRD PARTY LIBRARIES
import flask

# IMPORT LOCAL LIBRARIES
from lorgs.cache import cache
from lorgs.models.warcraftlogs_user_report import UserReport


blueprint = flask.Blueprint("api.user_reports", __name__)


def _get_user_report(report_id) -> UserReport:
    return UserReport.objects(report__report_id=report_id).first() # pylint: disable=no-member


@blueprint.route("/<string:report_id>")
@cache.cached(query_string=True)
def get_user_report(report_id):
    """Returns the overview about a user report.

    If specified Fights and Players can be included

    Query Args:
        fights[list[int], options]: list of fights to include
        players[list[int, optional]]: list of players to include

    """
    user_report = _get_user_report(report_id)
    if not user_report:
        return "Report not found.", 404

    info = user_report.as_dict()

    # include fights (if specified)
    info["fights"] = []
    for fight_id in flask.request.args.getlist("fight"):
        fight = user_report.report.get_fight(fight_id=int(fight_id))
        if fight:
            info["fights"].append(fight.as_dict())

    return info


@blueprint.route("/<string:report_id>/fights/<int:fight_id>")
@cache.cached()
def get_fight(report_id, fight_id):
    """Get a single fight from a report."""
    user_report = _get_user_report(report_id)
    if not user_report:
        return "Report not found.", 404

    fight = user_report.report.get_fight(fight_id=fight_id)
    return fight.as_dict()


@blueprint.route("/<string:report_id>/fights/<int:fight_id>/players/<int:source_id>")
@cache.cached()
def get_player(report_id, fight_id, source_id):
    """Get a single player from a fight."""
    user_report = _get_user_report(report_id)
    if not user_report:
        return "Report not found.", 404

    fight = user_report.report.get_fight(fight_id=fight_id)
    if not fight:
        return "Invalid Fight ID", 404

    player = fight.get_player(source_id=source_id)
    if not player:
        return "Invalid Source ID", 404

    return player.as_dict()
