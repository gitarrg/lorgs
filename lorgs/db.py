"""Module to setup our DB Connection."""

# IMPORT STANDARD LIBRARIES
import os

# IMPORT THIRD PARTY LIBRARIES
from pymongo import monitoring
import mongoengine as me

# IMPORT LOCAL LIBRARIES
from lorgs.logger import logger


class CommandLogger(monitoring.CommandListener):

    def started(self, event):
        logger.debug("{0.command_name} start".format(event))

    def succeeded(self, event):
        logger.debug("{0.command_name} succeeded in {0.duration_micros:g}μs".format(event))

    def failed(self, event):
        logger.debug("{0.command_name} failed in {0.duration_micros:g}μs".format(event))


# monitoring.register(CommandLogger())


URI = os.getenv("MONGO_URI")

if not URI:
    raise EnvironmentError("MONGO_URI not set!")

me.connect(host=URI)
