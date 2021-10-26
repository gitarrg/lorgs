"""Small Function to send error messges recived from pub/sub to Discord.

This needs some additional setup in the google console:

    1) PubSub --> create topic

    2) Logging / Logs Router --> create Sink
        create a sink that sends selected log messages to your pub sub topic
        eg.:
            >>> severity=ERROR
            >>> resource.type="gae_app"

    3) deploy this as a cloud function, subscribed to the topic


Deployment:
    as this function exists very unrelated to the actual lorrgs source code,
    it is deployed independently.

    I honestly just copy-pasted the source code from here into the online editor.

    Note:
        you need to setup a requirements.txt-file with at least:
        >>> requests==2.26.0


Help on Formatting: https://discohook.org/

"""
import requests
import base64
import os
import json


WEBHOOK_URL = os.getenv("WEBHOOK_URL")
AVATAR_URL = os.getenv("AVATAR_URL")
LOGS_BASE_URL = os.getenv("LOGS_BASE_URL")


COLORS = {
    "WARNING": 16763904,  # = "#ffcc00",
    "ERROR":   16724787,  # = "#b33636",
}



def add_field(name, value):
    if not value:
        return []

    return [{
        "name": name,
        "value": value,
    }]


def build_embed(data):
    severity = data.get("severity")

    return {
        "title": f"Google Log: {severity}",
        "color": COLORS.get(severity),
        "timestamp": data.get("timestamp"),

        "author": {
            "name": "Google Logs",
            "url": LOGS_BASE_URL,
            "icon_url": AVATAR_URL,
        },

        "fields": [],
    }

def build_embed_fields(data):

    fields = []

    payload = data.get("protoPayload", {})
    fields += add_field(name="Page", value=payload.get("referrer"))
    fields += add_field(name="Resource", value=payload.get("resource"))
    for line in payload.get("line", []):  # contains the error message
        fields += add_field(name="Message", value=line.get("logMessage"))

    text_payload = data.get("textPayload")
    if text_payload:
        error_messages = text_payload.split("\n")[-5:]
        error_messages = "\n".join(error_messages)
        error_messages = f"```\n{error_messages}\n```"
        fields += add_field(name="Traceback", value=error_messages)

    return fields


def send_message(event, context=None):
    """Triggered from a message on a Cloud Pub/Sub topic.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """

    # parse input data
    pubsub_message = base64.b64decode(event['data']).decode('utf-8')
    data = json.loads(pubsub_message)
    print("pubsub_message", pubsub_message)

    # build the embed
    embed = build_embed(data)
    embed["fields"] += build_embed_fields(data)

    # build the message
    discord_message = {}
    discord_message["embeds"] = [embed]

    ############################################################################
    # and send!
    requests.post(WEBHOOK_URL, json=discord_message)
