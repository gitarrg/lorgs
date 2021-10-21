"""Create and configure the Cache."""

# IMPORT THIRD PARTY LIBRARIES
import flask_caching


cache = flask_caching.Cache()


def init_app(app):
    cache.init_app(app)
