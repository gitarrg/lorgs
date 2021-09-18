# pylint: disable=too-few-public-methods

import os

class BaseConfig:
    """Default Config."""

    SECRET_KEY = os.environ.get("SECRET_KEY") or "giga-secret_key-nobody-will-ever-find-out"

    GOOGLE_ANALYTICS_ID = ""

    CACHE_DEFAULT_TIMEOUT = 300
    CACHE_TYPE = "SimpleCache"

    DISCORD_LINK = os.environ.get("DISCORD_LINK") or "https://discord.gg/U3xmktWEzU"

    # switch used to use non mimified js files
    LOCAL_FILES = False


################################################################################

class DevelopmentConfig(BaseConfig):
    """Config used for Development."""

    SEND_FILE_MAX_AGE_DEFAULT = 0  # for DEV. updates static files
    TEMPLATES_AUTO_RELOAD = True

    # pretty json (i just like them more)
    JSONIFY_PRETTYPRINT_REGULAR = True

    LOCAL_FILES = True

    CACHE_TYPE = "SimpleCache"
    CACHE_NO_NULL_WARNING = True


################################################################################


class ProductionConfig(BaseConfig):
    """Config used in Production."""

    GOOGLE_ANALYTICS_ID = "G-Y92VPCY6QW"

    CACHE_DEFAULT_TIMEOUT = 600  # 10min
