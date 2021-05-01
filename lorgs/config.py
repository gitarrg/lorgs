import os

# pylint: disable=too-few-public-methods

class BaseConfig:
    """Default Config"""

    # Flask Main
    SECRET_KEY = os.environ.get("SECRET_KEY") or "giga-secret_key-nobody-will-ever-find-out"


################################################################################

class DevelopmentConfig(BaseConfig):
    """Config used for Development."""

    GOOGLE_ANALYTICS_ID = ""
    SEND_FILE_MAX_AGE_DEFAULT = 0  # for DEV. updates static files


################################################################################


class ProductionConfig(BaseConfig):
    """Config used in Production."""

    GOOGLE_ANALYTICS_ID = "G-Y92VPCY6QW"
