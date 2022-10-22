import os
import aiohttp


DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")


async def main(message):
    if not DISCORD_WEBHOOK_URL:
        raise EnvironmentError("Missing DISCORD_WEBHOOK_URL")

    data = {
        "embeds" : [{
            "fields": [
                {"name": "ID", "value": message.get("messageId")},
                {"name": "Body", "value": message.get("body")}
            ]
        }]
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url=DISCORD_WEBHOOK_URL, json=data):
            pass

