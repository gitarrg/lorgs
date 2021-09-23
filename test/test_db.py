
# IMPORT STANDARD LIBRARIES
import os

# IMPORT THIRD PARTY LIBRARIES
# from flask_sqlalchemy import SQLAlchemy
import arrow
import dotenv
dotenv.load_dotenv() # pylint: disable=wrong-import-position

# IMPORT LOCAL LIBRARIES
from lorgs import db
from lorgs import data
from lorgs import utils
from lorgs.models import warcraftlogs_ranking
from lorgs.models import warcraftlogs_comps
from lorgs.models import specs
from lorgs.models import encounters



def delete_old_spec_rankings():
    """Remove old spec rankings."""
    for boss in data.CASTLE_NATHRIA_BOSSES:
        print(boss)
        for spec_ranking in warcraftlogs_ranking.SpecRanking.objects(boss_slug=boss.name_slug).all():
            print("\t", spec_ranking.spec_slug, spec_ranking.boss_slug)
            spec_ranking.delete()


if __name__ == '__main__':
    pass
