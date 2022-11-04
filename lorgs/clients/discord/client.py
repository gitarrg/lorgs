"""Very Basic Discord "client"."""

# IMPORT STANDARD LIBRARIES
from email import message
import os
import typing

# IMPORT THIRD PARTY LIBRARIES
import aiohttp

from lorgs.clients.discord.models import (
    DiscordGuildMember,
    DiscordUser,
    DiscordAccessTokenResponse,
    DiscordErrorResponse,
)

API_URL = "https://discordapp.com/api"

DISCORD_CLIENT_ID = os.getenv("DISCORD_CLIENT_ID")
DISCORD_CLIENT_SECRET = os.getenv("DISCORD_CLIENT_SECRET")
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")


################################################################################
# Core
#

async def api_request(
    endpoint: str,
    headers: typing.Optional[dict[str, typing.Any]] = None,
    data: typing.Optional[dict[str, typing.Any]] = None,
    method="GET"
):
    """Perform a generic request to the Discord API."""
    url = f"{API_URL}/{endpoint}"
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.request(method, url, data=data) as resp:
            return await resp.json()


async def bot_request(endpoint: str):
    """Helper to run any reuqest via out bot-account."""
    headers = {"Authorization": f"Bot {DISCORD_BOT_TOKEN}"}
    return await api_request(endpoint, headers=headers)


################################################################################
#   Auth
#


async def exchange_code(code: str, redirect_uri: str) -> typing.Union[DiscordAccessTokenResponse, DiscordErrorResponse]:
    """Exchange a code for an user access token.

    ref: https://discord.com/developers/docs/topics/oauth2#authorization-code-grant-access-token-exchange-example
    """
    data = {
        'client_id': DISCORD_CLIENT_ID,
        'client_secret': DISCORD_CLIENT_SECRET,
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': redirect_uri,
        "scope": "identify"
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    return await api_request(  # type: ignore
        endpoint="oauth2/token",
        method="post",
        headers=headers,
        data=data,
    )

################################################################################
#   User Info
#

async def get_user_profile(access_token: str) -> DiscordUser:
    """Get the logged in user's discord profile

    Args:
        access_token: bearer token recied from the OAuth2

    ref: https://discord.com/developers/docs/resources/user#get-current-user

    Example Response (omitted some fields):
        >>> {
        >>>   "id": "80351110224678912",
        >>>   "username": "Nelly",
        >>>   ...
        >>> }
    """
    headers = {
        'Authorization': f"Bearer {access_token}",
    }

    response = await api_request(
        endpoint="users/@me",
        headers=headers
    )

    message = response.get("message") or ""
    if "Unauthorized" in message:
        raise PermissionError(message)

    return DiscordUser.parse_obj(response)


async def get_user_info(user_id: int) -> DiscordUser:
    """Get the User Info.

    ref: https://discord.com/developers/docs/resources/user#get-user

    Example (omitted some fields):
        >>> await get_user_info(248163264)
        {
            id: 248163264,
            username: "Arrg",
            avatar: "132132323"
        }
    """
    url = f"users/{user_id}"
    response = await bot_request(url)
    return DiscordUser.parse_obj(response)


################################################################################
#   Guild Member Info
#

async def get_member_info(server_id: int, user_id: int) -> DiscordGuildMember:
    """Get the Member Info about a user in a Discord Server.

    This will return information like member-roles, nickname joined date etc.
    ref: https://discord.com/developers/docs/resources/guild#get-guild-member

    Args:
        server_id (int): ID of the Discord Server
        user_id (int): ID of the User

    Example (omitted some fields):
        >>> await get_member_info(248163264)
        {
            "user": {
                id: 248163264,
                username: "Arrg",
            },
            "nick": "Arrgmin",
            "roles": [123123123, 234234234234, 456456456],
            "joined_at": "2015-04-26T06:26:56.936000+00:00",
        }
    """
    print("GET_MEMBER_INFO", server_id, user_id)

    url = f"guilds/{server_id}/members/{user_id}"
    response = await bot_request(url)

    message = response.get("message")
    if message:
        raise ValueError(message)

    return DiscordGuildMember.parse_obj(response)



