"""Create and configure the Cache."""

# IMPORT THIRD PARTY LIBRARIES
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend


def init(config):
    backend = InMemoryBackend()
    FastAPICache.init(backend, expire=config.CACHE_DEFAULT_TIMEOUT)
    return FastAPICache
