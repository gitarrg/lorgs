
import os

# pylint: disable=too-few-public-methods

class Config:
    """Default Config"""

    # Flask Main
    SECRET_KEY = os.environ.get("SECRET_KEY") or "giga-secret_key-nobody-will-ever-find-out"

    # Flask-Caching
    # CACHE_TYPE = "SimpleCache"
    CACHE_DEFAULT_TIMEOUT = 0  # no timeouts! :yaaah:
    CACHE_TYPE = "RedisCache"

    CACHE_REDIS_HOST = os.getenv("REDIS_HOST") or "localhost"
    CACHE_REDIS_PORT = os.getenv("REDIS_PORT") or 6379
    CACHE_REDIS_PASSWORD = os.getenv("REDIS_PASS")
    CACHE_REDIS_DB = os.getenv("REDIS_DB")


################################################################################


class DevelopmentConfig(Config):

    GOOGLE_ANALYTICS_ID = ""
    SEND_FILE_MAX_AGE_DEFAULT = 0  # for DEV. updates static files


################################################################################


class ProductionConfig(Config):

    GOOGLE_ANALYTICS_ID = "G-Y92VPCY6QW"


class HerokuProductionConfig(ProductionConfig):

    DATABASE_URI = 'mysql://user@localhost/foo'

    CACHE_OPTIONS = {
        "ssl": True,
        "ssl_cert_reqs": None
    }
