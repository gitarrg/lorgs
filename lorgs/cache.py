"""Create and configure the Cache."""

# IMPORT STANDARD LIBRARIES
import os
import json

# IMPORT THIRD PARTY LIBRARIES
import redis

# IMPORT LOCAL LIBRARIES
from lorgs.logger import logger

# REDIS_HOST = os.getenv("REDIS_HOST") or "localhost"
# REDIS_PORT = os.getenv("REDIS_PORT") or 6379
# REDIS_USER = os.getenv("REDIS_USER")
# REDIS_PASS = os.getenv("REDIS_PASS")
# REDIS_DB = os.getenv("REDIS_DB")

class RedisJsonCache:
    """docstring for RedisCache"""
    def __init__(self, host="", port=0, user="", password="", **kwargs):
        super().__init__()

        host = host or os.getenv("REDIS_HOST") or "localhost"
        port = port or os.getenv("REDIS_PORT") or 6379
        user = user or os.getenv("REDIS_USER") or ""
        password = password or os.getenv("REDIS_PASS") or ""

        if "productuon" in os.getenv("LORGS_CONFIG_NAME", "").lower():
            kwargs["ssl"] = True
            kwargs["ssl_cert_reqs"] = None

        self.client = redis.StrictRedis(
            host=host,
            port=port,
            username=user,
            password=password,
            **kwargs
        )

    def set(self, key, data, timeout=None):
        self.client.set(key, json.dumps(data), ex=timeout)

    def get(self, key):
        data = self.client.get(key)
        return json.loads(data) if data else None


Cache = RedisJsonCache()
