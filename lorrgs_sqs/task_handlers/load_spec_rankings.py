"""Handler to Load Spec Rankings."""

# IMPORT STANDARD LIBRARIES
import json

# IMPORT LOCAL LIBRARIES
from lorgs import data  # pylint: disable=unused-import
from lorgs import db  # pylint: disable=unused-import
from lorgs.models import warcraftlogs_ranking


async def load_spec_rankings(
    boss_slug: str, spec_slug: str,
    difficulty = "mythic", metric = "dps",
    limit = 50, clear = False,
    **kwargs, # pylint: disable=unused-argument
):
    """Load the Spec Ranking Data from Warcraftlogs and save it to the Database."""
    ################################
    # Get inputs
    print(f"loading: {boss_slug} vs {spec_slug} | (difficulty={difficulty} / metric={metric} / limit={limit} / clear={clear})")
    if boss_slug is None or spec_slug is None:
        return f"missing boss or spec ({boss_slug} / {spec_slug})"

    ################################
    # get spec ranking object
    ranking = warcraftlogs_ranking.SpecRanking.get_or_create(
        boss_slug=boss_slug,
        spec_slug=spec_slug,
        difficulty=difficulty,
        metric=metric,
    )
    if not ranking.boss:
        return "invalid boss"
    if not ranking.spec:
        return "invalid spec"

    ################################
    # load and save
    await ranking.load(limit=limit, clear_old=clear)
    ranking.save()
    return "done"


async def main(message):
    message_body = message.get("body")
    message_payload = json.loads(message_body)
    await load_spec_rankings(**message_payload)
