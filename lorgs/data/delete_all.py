#!/usr/bin/env python

# IMPORT THIRD PARTY LIBRARIES
import dotenv
dotenv.load_dotenv() # pylint: disable=wrong-import-position

from lorgs.app import create_app
from lorgs.db import db
from lorgs.models.encounters import RaidBoss
from lorgs.models.encounters import RaidZone
from lorgs.models.specs import WowClass
from lorgs.models.specs import WowRole
from lorgs.models.specs import WowSpec
from lorgs.models.specs import WowSpec
from lorgs.models.specs import WowSpell


def main():
    app = create_app()
    with app.app_context():

        # encounters
        RaidBoss.query.delete()
        RaidZone.query.delete() # includes Bosses

        # specs
        WowSpell.query.delete()
        WowSpec.query.delete()
        WowClass.query.delete()
        WowRole.query.delete()

        db.session.commit()
        print("DELETED", db.session.deleted)


if __name__ == '__main__':
    main()
