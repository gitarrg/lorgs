"""Module to setup our DB Connection."""

# IMPORT STANDARD LIBRARIES
import os
from contextlib import contextmanager

# IMPORT THIRD PARTY LIBRARIES
import sqlalchemy
from sqlalchemy import orm
from sqlalchemy.ext.declarative import declarative_base

# IMPORT LOCAL LIBRARIES
from lorgs.logger import logger


URI = os.getenv("SQLALCHEMY_DATABASE_URI") or "sqlite://"

engine = sqlalchemy.create_engine(URI, pool_recycle=240)
factory = orm.sessionmaker(bind=engine, autoflush=True)
session = orm.scoped_session(factory)

Base = declarative_base()
Base.query = session.query_property()


# for debugging
_QUERY_COUNT = 0
def count_queries(*args, **kwargs):
    global _QUERY_COUNT
    _QUERY_COUNT += 1
    logger.info("QUERY COUNT: %d", _QUERY_COUNT)

# if DEBUG
# sqlalchemy.event.listen(Engine, "before_cursor_execute", count_queries)


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
