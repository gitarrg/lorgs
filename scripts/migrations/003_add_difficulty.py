#!/usr/bin/env python
"""Util to fill in some missing data."""
import dotenv
dotenv.load_dotenv() # pylint: disable=wrong-import-position

# from lorgs import data
from lorgs import db
from lorgs.models import warcraftlogs_ranking

########################################
#
#
def load_spec_rankings(limit=None):

    print("load_spec_rankings START")

    rankings = warcraftlogs_ranking.SpecRanking.objects(difficulty=None)
    if limit:
        rankings = rankings[:limit]
    print("rankings", rankings)
    for ranking in rankings:
        ranking.difficulty = ranking.difficulty or "mythic"
        print("ranking", ranking.spec_slug, ranking.boss_slug, ranking.difficulty)
        ranking.save()
    print("load_spec_rankings DONE")


if __name__ == '__main__':
    load_spec_rankings()
