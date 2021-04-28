"""Create all the initial DB Data."""
# pylint: disable=wrong-import-position,invalid-name

# IMPORT STANDARD LIBRARIES

# IMPORT THIRD PARTY LIBRARIES
import dotenv
dotenv.load_dotenv()

# IMPORT LOCAL LIBRARIES
from lorgs.app import create_app
from lorgs.models.specs import WowRole, WowClass, WowSpec, WowSpell
from lorgs.db import db


from init_data import init_classes
from init_data import init_encounters

# create app instance
app = create_app()
app.app_context().push()



def delete_all():

    # RaidBoss.query.delete()
    # RaidZone.query.delete()

    # WowSpec.__table__.drop()
    # WowClass.__table__.drop()
    # WowRole.__table__.drop()
    db.drop_all()
    db.create_all()
    # WowSpec.query.delete()
    # WowClass.query.delete()
    # WowRole.query.delete()
    db.session.commit()



def create_all():

    init_classes.create()
    init_encounters.create()

    db.session.commit()

    init_classes.load_spell_icons()
    db.session.commit()




if __name__ == '__main__':

    delete_all()
    create_all()

    # test2()
    # load_spell_icons()
