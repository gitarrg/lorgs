"""Create all the initial DB Data."""
# pylint: disable=wrong-import-position,invalid-name

# IMPORT STANDARD LIBRARIES

# IMPORT THIRD PARTY LIBRARIES
import dotenv
dotenv.load_dotenv()

# IMPORT LOCAL LIBRARIES
from lorgs.app import create_app
# from lorgs.models.encounters import RaidZone, RaidBoss
from lorgs.models.specs import WowRole, WowClass, WowSpec, WowSpell
from lorgs.models.reports import Report, Fight, Player, Cast
from lorgs.db import db


# create app instance
app = create_app()



with app.app_context():


    # Cast.query.delete()
    bind = db.session.bind

    for cls in (Cast, Player, Fight, Report):
        try:
            cls.__table__.drop(bind)
        except Exception as e:
            print("unable to drop table", cls, e)
    """
    """
    # Delete
    # Report.__table__.drop()
    # Fight.__table__.drop()

    # db.drop_all(tables=tables)
    db.create_all()
    db.session.commit()


# recreate
# db.create_all()
print("done")


