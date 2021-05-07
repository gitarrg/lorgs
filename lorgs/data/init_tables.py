#!/usr/bin/env python
"""Models for Raids and RaidBosses."""

# IMPORT THIRD PARTY LIBRARIES
import dotenv
dotenv.load_dotenv() # pylint: disable=wrong-import-position

# IMPORT LOCAL LIBRARIES
from lorgs import db

# we need to import them, so sqlalchemy is aware these models exist
from lorgs.models import encounters
from lorgs.models import specs
from lorgs.models import warcraftlogs
from lorgs.models import warcraftlogs_ranking

db.Base.metadata.create_all(db.engine)
