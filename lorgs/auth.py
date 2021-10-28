"""Module to deal with Auth.

We use Discords OAuuth2 Endpoints, to allow users to sign in via discord:
Docs: https://discord.com/developers/docs/topics/oauth2

"""
import os
import typing
import aiohttp

################################################################################
#   Settings
#

DISCORD_CLIENT_ID = os.getenv("DISCORD_CLIENT_ID")
DISCORD_CLIENT_SECRET = os.getenv("DISCORD_CLIENT_SECRET")
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
DISCORD_API = "https://discordapp.com/api"
REDIRECT_URI = "https://lorrgs.nw.r.appspot.com/"


# int: server ID for the lorgs disocrd.
LORRGS_SERVER_ID  = 885638678607708172

# Role IDs:
# used to check what features a logged-in user can access
ROLE_ID_MOD       = 885660390120362024  # Morrgerator
ROLE_ID_ADMIN     = 885660648510455839  # Arrgmin
ROLE_ID_PATREON   = 886595672525119538  # Investorrg


################################################################################
#   Helpers
#

async def _run_api_request(
        endpoint: str,
        headers: typing.Dict[str, typing.Any] = None,
        data: typing.Dict[str, typing.Any] = None,
        method="GET"
    ):
    """Perform a generic request to the Discord API."""
    url = f"{DISCORD_API}/{endpoint}"
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.request(method, url, data=data) as resp:
            return await resp.json()


async def _run_bot_request(endpoint):
    """Helper to run any reuqest via out bot-account."""
    # url = f"{DISCORD_API}/{endpoint}"
    headers = {"Authorization": f"Bot {DISCORD_BOT_TOKEN}"}
    return await _run_api_request(endpoint, headers=headers)


################################################################################
#   Auth
#


async def exchange_code(code):
    """Exchange a code for an user access token.

    ref: https://discord.com/developers/docs/topics/oauth2#authorization-code-grant-access-token-exchange-example

    Response:
        >>> {
        >>>     "access_token": "<ACCESS_TOKEN>",
        >>>     "token_type": "Bearer",
        >>>     "expires_in": 604800,
        >>>     "refresh_token": "<REFRESH_TOKEN>",
        >>>     "scope": "identify"
        >>> }
    """
    data = {
        'client_id': DISCORD_CLIENT_ID,
        'client_secret': DISCORD_CLIENT_SECRET,
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI,
        "scope": "identify"
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    return await _run_api_request(
        endpoint="oauth2/token",
        method="post",
        headers=headers,
        data=data,
    )


async def get_user_profile(access_token: str):
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

    return await _run_api_request(
        endpoint="users/@me",
        headers=headers,
    )


################################################################################
#   User/Member Info
#


async def get_member_info(user_id):
    """Get the Member Info about a user in the Lorrgs Discord.

    This will return information like member-roles, nickname joined date etc.

    ref: https://discord.com/developers/docs/resources/guild#get-guild-member

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
    url = f"guilds/{LORRGS_SERVER_ID}/members/{user_id}"
    return await _run_bot_request(url)


async def get_member_roles(user_id: int) -> typing.List[str]:
    """Get the roles a given user has in the Lorrgs Discord.

    Note:
        the role ids are returned as strings

    """
    member_info = await get_member_info(user_id=user_id)
    return member_info.get("roles", [])


async def get_member_features(user_id):
    """Check which features a given user is allows to use."""
    roles = await get_member_roles(user_id=user_id)
    features = {}
    features["admin"] = str(ROLE_ID_ADMIN) in roles
    features["mod"] = str(ROLE_ID_MOD) in roles
    features["patreon"] = str(ROLE_ID_PATREON) in roles
    return features
