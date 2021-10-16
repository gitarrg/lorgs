# pylint: disable=too-few-public-methods

import os


class BaseConfig:
    """Default Config."""

    SECRET_KEY = os.getenv("SECRET_KEY") or "giga-secret_key-nobody-will-ever-find-out"

    # cache settings
    CACHE_DEFAULT_TIMEOUT = 5 * 60 # seconds
    CACHE_TYPE = "SimpleCache"

    JSONIFY_PRETTYPRINT_REGULAR = False

    # bool: use dev files
    LORRGS_DEBUG = False


################################################################################

class DevelopmentConfig(BaseConfig):
    """Config used for Development."""

    # bool: use dev files
    LORRGS_DEBUG = True

    SEND_FILE_MAX_AGE_DEFAULT = 0  # for DEV. updates static files
    SEND_FILE_MAX_AGE_DEFAULT = 1000
    TEMPLATES_AUTO_RELOAD = True

    CACHE_TYPE = "SimpleCache" # NullCache
    CACHE_NO_NULL_WARNING = True


################################################################################


class ProductionConfig(BaseConfig):
    """Config used in Production."""
    CACHE_DEFAULT_TIMEOUT = 60 * 60  # 1h
