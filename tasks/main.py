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
from lorgs.models import warcraftlogs_ranking



def load_spec_rankings(request):
    """Load the Spec Ranking Data from Warcraftlogs and save it to the Database.

    Arguments should be passed as request args.
    Args:
        boss_slug (str)
        spec_slug (str)
        limit (int, optional): default=50
        clear (bool, optional): default=False

    """
    # Get inputs
    boss_slug = request.args.get("boss_slug", type=str)
    spec_slug = request.args.get("spec_slug", type=str)
    limit = request.args.get("limit", type=int, default=50)
    clear = request.args.get("clear", default=False, type=json.loads)
    print(f"loading: {boss_slug} vs {spec_slug} | (limit={limit})")
    if boss_slug is None or spec_slug is None:
        return f"missing boss or spec ({boss_slug} / {spec_slug})"

    # get spec ranking object
    ranking = warcraftlogs_ranking.SpecRanking.get_or_create(boss_slug=boss_slug, spec_slug=spec_slug)
    if not ranking.boss:
        return "invalid boss"
    if not ranking.spec:
        return "invalid spec"

    # load and save
    task = ranking.load(limit=limit, clear_old=clear)
    asyncio.run(task)
    ranking.save()

    return "done"
