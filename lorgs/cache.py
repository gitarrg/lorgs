"""Create and configure the Cache."""

# IMPORT THIRD PARTY LIBRARIES
import flask_caching

# IMPORT LOCAL LIBRARIES
from lorgs.logger import logger


Cache = flask_caching.Cache(
    config={'CACHE_TYPE': 'RedisCache'},



)


def init_app(app):
    logger.info("init Cache")
    Cache.init_app(app)
