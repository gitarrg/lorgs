"""Create and configure the Cache."""

# IMPORT STANDARD LIBRARIES
import os
import json

# IMPORT THIRD PARTY LIBRARIES
import redis

# IMPORT LOCAL LIBRARIES
from lorgs.logger import logger


class RedisJsonCache:
    """docstring for RedisCache"""
    def __init__(self, url=""):
        super().__init__()

        url = url or os.getenv("REDISCLOUD_URL") or "redis://localhost:6379"
        self.client = redis.StrictRedis.from_url(url)

    def set(self, key, data, timeout=None):
        self.client.set(key, json.dumps(data), ex=timeout)

    def get(self, key):
        data = self.client.get(key)
        return json.loads(data) if data else None


Cache = RedisJsonCache()
