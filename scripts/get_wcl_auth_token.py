#!/usr/bin/env python
"""Generate a token to be used with Desktop Clients like Insomnia."""

import asyncio

import dotenv
dotenv.load_dotenv() # pylint: disable=wrong-import-position

from lorgs.clients.wcl import WarcraftlogsClient


async def main() -> None:
    c = WarcraftlogsClient()
    await c.update_auth_token()
    print(c.headers["Authorization"])


if __name__ == '__main__':
    asyncio.run(main())
