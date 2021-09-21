# pylint: disable=too-few-public-methods

import os

class BaseConfig:
    """Default Config."""

    SECRET_KEY = os.getenv("SECRET_KEY") or "giga-secret_key-nobody-will-ever-find-out"

    GOOGLE_ANALYTICS_ID = ""

    CACHE_DEFAULT_TIMEOUT = 300
    CACHE_TYPE = "SimpleCache"

    DISCORD_LINK = os.getenv("DISCORD_LINK") or "https://discord.gg/U3xmktWEzU"

    # switch used to use non mimified js files
    LOCAL_FILES = False

    # custom tag to force refreshes on js and css files
    BUILD_TAG = os.getenv("BUILD_TAG", "BUILD_TAG")


################################################################################

class DevelopmentConfig(BaseConfig):
    """Config used for Development."""

    SEND_FILE_MAX_AGE_DEFAULT = 0  # for DEV. updates static files
    TEMPLATES_AUTO_RELOAD = True

    # pretty json (i just like them more)
    JSONIFY_PRETTYPRINT_REGULAR = True

    LOCAL_FILES = True

    CACHE_TYPE = "NullCache"
    CACHE_NO_NULL_WARNING = True


################################################################################


class ProductionConfig(BaseConfig):
    """Config used in Production."""

    GOOGLE_ANALYTICS_ID = "G-Y92VPCY6QW"

    CACHE_DEFAULT_TIMEOUT = 600  # 10min
