"""Entry points for all our Cloud Functions.

    Note:
        this file has to be called "main.py"

"""
# IMPORT STANDARD LIBRARIES
import asyncio
import json

# IMPORT THIRD PARTY LIBRARIES

# IMPORT LOCAL LIBRARIES
from lorgs import db   # pylint: disable=unused-import
from lorgs import data # pylint: disable=unused-import
from lorgs import utils
from lorgs.models import warcraftlogs_ranking
from lorgs.models.warcraftlogs_user_report import UserReport
from lorgs.models.warcraftlogs_comp_ranking import CompRanking


def to_bool(s):
    return s.lower() in ["true", "1", "y", "yes"]


def load_spec_rankings(request):
    """Load the Spec Ranking Data from Warcraftlogs and save it to the Database.

    Arguments should be passed as request args.
    Args:
        boss_slug (str)
        spec_slug (str)
        limit (int, optional): default=50
        clear (bool, optional): default=False

    """
    ################################
    # Get inputs
    boss_slug = request.args.get("boss_slug", type=str)
    spec_slug = request.args.get("spec_slug", type=str)
    difficulty = request.args.get("difficulty", type=str) or "mythic"
    limit = request.args.get("limit", type=int, default=50)

    clear = request.args.get("clear", default=False, type=to_bool)
    print(f"loading: {boss_slug} vs {spec_slug} | (difficulty={difficulty} / limit={limit} / clear={clear})")
    if boss_slug is None or spec_slug is None:
        return f"missing boss or spec ({boss_slug} / {spec_slug})"

    ################################
    # get spec ranking object
    ranking = warcraftlogs_ranking.SpecRanking.get_or_create(
        boss_slug=boss_slug,
        spec_slug=spec_slug,
        difficulty=difficulty,
    )
    if not ranking.boss:
        return "invalid boss"
    if not ranking.spec:
        return "invalid spec"

    ################################
    # load and save
    task = ranking.load(limit=limit, clear_old=clear)
    asyncio.run(task)
    ranking.save()

    return "done"


def load_comp_rankings(request):
    """Load Comp Rankings from Warcraftlogs and save them in our DB.

    Query Parms:
        boss_slug (str): name of the boss (full_name_slug)
        limit (int): maximum number of fights to fetch (default: 100)
        clear (bool): delete old fights (default: false)

    """
    ################################
    # Get inputs
    boss_slug = request.args.get("boss_slug", type=str)
    limit = request.args.get("limit", type=int, default=200)
    clear = request.args.get("clear", default=False, type=to_bool)

    ################################
    # get comp ranking object
    print(f"[load_comp_rankings] boss_slug={boss_slug} limit={limit} limit={limit}")
    comp_ranking = CompRanking.get_or_create(boss_slug=boss_slug)

    ################################
    # load and save
    task = comp_ranking.load(limit=limit, clear_old=clear)
    asyncio.run(task)
    comp_ranking.save()
    return {"status": "done", "task_id": "done"}


def load_user_report(request):
    """Load a Report

    Args:
        report_id(str): the report to load
        fights[list(int)]: fight ids
        player[list(int)]: player ids

    """
    ################################
    # parse inputs
    report_id = request.args.get("report_id", type=str)
    fight_ids = request.args.get("fight", type=utils.str_int_list)
    player_ids = request.args.get("player", type=utils.str_int_list)

    print(f"[load_user_report] report_id={report_id} fight_ids={fight_ids} player_ids={player_ids}")
    if not (report_id and fight_ids and player_ids):
        return "Missing fight or player ids", 400

    ################################
    # loading...
    user_report = UserReport.from_report_id(report_id=report_id, create=True)
    task = user_report.report.load_fights(fight_ids=fight_ids, player_ids=player_ids)
    asyncio.run(task)
    user_report.save()
    return {"status": "done", "task_id": "done"}
