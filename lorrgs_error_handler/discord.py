"""Format and send the Discord Message.

Help on Formatting: https://discohook.org/
"""
from datetime import datetime
from urllib import request
import json
import os


WEBHOOK_URL = os.getenv("WEBHOOK_URL")


def add_field(name, value):
    """Create an Embed Field."""
    if not value:
        return []

    return [{
        "name": name,
        "value": value,
    }]


def send_message(payload):
    """Triggered from a message on a Cloud Pub/Sub topic."""
    # build the embed
    embed = {
        "title": "Error",
        "color": 16724787,  # = "#b33636",
        "fields": [],
    }

    fields = []
    fields += add_field("logGroup", payload.get("logGroup"))
    fields += add_field("logStream", payload.get("logStream"))


    for event in payload.get("logEvents") or []:

        timestamp = event.get("timestamp")
        event_time = datetime.fromtimestamp(timestamp / 1000)
        fields += add_field("timestamp", event_time.isoformat())

        # Get last 5 lines and wrap in a code block
        message = event.get("message") or ""
        message = message.split("\n")[-5:]
        message = "\n".join(message)
        message = f"```\n{message}\n```"
        fields += add_field("message", message)

    embed["fields"] = fields


    # build the message
    discord_message = {}
    discord_message["embeds"] = [embed]

    ############################################################################
    # and send!
    data = json.dumps(discord_message).encode("utf-8")

    response = request.Request(WEBHOOK_URL, data=data)

    # https://stackoverflow.com/a/65843620
    response.add_header('Content-Type', 'application/json')
    response.add_header('User-Agent', 'Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11')

    request.urlopen(response)
