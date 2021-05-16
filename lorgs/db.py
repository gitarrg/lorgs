"""Module to setup our DB Connection."""

# IMPORT STANDARD LIBRARIES
import os
# from contextlib import contextmanager

# IMPORT THIRD PARTY LIBRARIES
from pymongo import monitoring
# from mongoengine import *
import mongoengine as me

# import sqlalchemy
# from sqlalchemy import orm
# from sqlalchemy.ext.declarative import declarative_base

# IMPORT LOCAL LIBRARIES
# from lorgs import utils
from lorgs.logger import logger


# log = logging.getLogger()
# log.setLevel(logging.DEBUG)
# logging.basicConfig(level=logging.DEBUG)


class CommandLogger(monitoring.CommandListener):

    def started(self, event):
        logger.debug("{0.command_name} start".format(event))

    def succeeded(self, event):
        logger.debug("{0.command_name} succeeded in {0.duration_micros:g}μs".format(event))

    def failed(self, event):
        logger.debug("{0.command_name} failed in {0.duration_micros:g}μs".format(event))


monitoring.register(CommandLogger())


URI = os.getenv("MONGO_URI")
# logger.warning("CONNECT TO MONGO_URI: %s", URI)
me.connect(host=URI)



################################################################################
################################################################################
################################################################################
'''
URI = os.getenv("SQLALCHEMY_DATABASE_URI") or "postgresql://"

engine = sqlalchemy.create_engine(URI, pool_recycle=240)
factory = orm.sessionmaker(bind=engine, autoflush=True)
session = orm.scoped_session(factory)


class BaseModel:

    @classmethod
    def get(cls, **kwargs):
        return utils.get(cls.query.all(), **kwargs)



Base = declarative_base(cls=BaseModel)
Base.query = session.query_property()


# for debugging
_QUERY_COUNT = 0
def count_queries(*args, **kwargs):
    global _QUERY_COUNT
    _QUERY_COUNT += 1
    logger.info("QUERY COUNT: %d", _QUERY_COUNT)

# if DEBUG
# sqlalchemy.event.listen(engine, "before_cursor_execute", count_queries)

@contextmanager
def session_context(commit=True):
    """Provide a transactional scope around a series of operations."""
    try:
        yield session

        if commit:
            session.commit()

    except:
        session.rollback()
        raise

    finally:
        session.remove()


def init_flask_app(app):
    """Add the listener to remove sessions on the end of a request."""
    @app.teardown_appcontext
    def shutdown_session(response_or_exc):
        session.remove()
        return response_or_exc

'''