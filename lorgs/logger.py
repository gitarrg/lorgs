"""Define and setup Logger-Instances."""
import os
import logging
import datetime


LOG_FORMAT = "[%(reltime)s][%(name)s] %(levelname)s: %(message)s"
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
"""
"""
# logger.setLevel(logging.DEBUG)
