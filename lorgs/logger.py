"""Define and setup Logger-Instances."""
from typing import Callable
import datetime
import functools
import inspect
import logging
import os
import time


LOG_FORMAT = "[%(reltime)s][%(name)s] %(levelname)s: [%(funcName)s] %(message)s"
"""str: Format to be used for log messages."""


class DeltaTimeFormatter(logging.Formatter):
    def format(self, record):
        duration = datetime.datetime.utcfromtimestamp(record.relativeCreated / 1000)
        record.reltime = duration.strftime("%M:%S.%f")[:7]
        return super().format(record)


logger = logging.getLogger("Lorgs")
"""The logger to log logging related log messages."""

formatter = DeltaTimeFormatter(LOG_FORMAT)

handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)

if os.getenv("DEBUG"):
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.INFO)



def timeit(func: Callable) -> Callable:

    is_async = inspect.iscoroutinefunction(func)
    if is_async:
        @functools.wraps(func)
        async def wrapped(*args, **kwargs):
            logger.debug(f"{func.__name__}: start")
            start = time.time()

            r = await func(*args, **kwargs)

            end = time.time()
            ms = (end-start) * 1000
            logger.info(f"{func.__name__}: done | time: {ms:0.3f}ms")

            return r
    else:
        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            logger.debug(f"{func.__name__}: start")
            start = time.time()

            r = func(*args, **kwargs)

            end = time.time()
            ms = (end-start) * 1000
            logger.info(f"{func.__name__}: done | time: {ms:0.3f}ms")

            return r

    return wrapped
