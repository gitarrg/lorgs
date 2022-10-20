import os
import aiohttp


WEBHOOK_URL = os.getenv("WEBHOOK_URL")



async def main(message):
    fields = [
        {"name": "ID", "value": message.get("messageId")},
        {"name": "Body", "value": message.get("body")}
    ]

    data = {
        # "content": "Hello!",
        "embeds" : [{
            "fields": fields
        }]
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url=WEBHOOK_URL, json=data):
            pass


if __name__ == "__main__":
    import asyncio
    asyncio.run(
        main({
            "messageId": "123-456",
            "body": "Test Message"
        })
    )



