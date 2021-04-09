"""Define and setup Logger-Instances."""
import os
import logging
import time
import datetime
import logging.handlers


LOG_FORMAT = "[%(reltime)s][%(name)s] %(levelname)s: %(message)s"
"""str: Format to be used for log messages."""


class DeltaTimeFormatter(logging.Formatter):
    def format(self, record):
        duration = datetime.datetime.utcfromtimestamp(record.relativeCreated / 1000)
        record.reltime = duration.strftime("%M:%S.%f")[:9]
        return super().format(record)


logger  = logging.getLogger("Lorrgs")
"""The logger to log logging related log messages."""

formatter = DeltaTimeFormatter(LOG_FORMAT)

handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)



logger.setLevel(logging.INFO)
"""
if os.getenv("DEBUG"):
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.INFO)
"""

if __name__ == '__main__':
    pass
    logger.warning("A")
    time.sleep(0.5)
    logger.warning("B")
    time.sleep(2.5)
    logger.warning("C")

