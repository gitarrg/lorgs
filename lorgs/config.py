# pylint: disable=too-few-public-methods

import os


class BaseConfig:
    """Default Config."""

    SECRET_KEY = os.getenv("SECRET_KEY") or "giga-secret_key-nobody-will-ever-find-out"

    # str: id for google analytics
    GOOGLE_ANALYTICS_ID = ""

    # str: discord invite link
    DISCORD_LINK = os.getenv("DISCORD_LINK") or "https://discord.gg/jZWj6djJk2"

    # cache settings
    CACHE_DEFAULT_TIMEOUT = 5 * 60 # seconds
    CACHE_TYPE = "SimpleCache"

    JSONIFY_PRETTYPRINT_REGULAR = False

    # switch used to use non mimified js files
    LOCAL_FILES = False

    # custom tag to force refreshes on js and css files
    BUILD_TAG = os.getenv("BUILD_TAG", "BUILD_TAG")


################################################################################

class DevelopmentConfig(BaseConfig):
    """Config used for Development."""

    # bool: use local/dev files
    LOCAL_FILES = True

    SEND_FILE_MAX_AGE_DEFAULT = 0  # for DEV. updates static files
    SEND_FILE_MAX_AGE_DEFAULT = 1000
    TEMPLATES_AUTO_RELOAD = True

    CACHE_TYPE = "SimpleCache" # NullCache
    CACHE_NO_NULL_WARNING = True


################################################################################


class ProductionConfig(BaseConfig):
    """Config used in Production."""

    GOOGLE_ANALYTICS_ID = "G-Y92VPCY6QW"

    CACHE_DEFAULT_TIMEOUT = 60 * 60  # 1h
