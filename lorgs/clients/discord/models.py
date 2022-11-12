import typing
from pydantic import BaseModel


class DiscordUser(BaseModel):
    """
    https://discord.com/developers/docs/resources/user#user-object
    """

    id: str
    username: str
    discriminator: str

    avatar: typing.Optional[str] = ""
    """the user's avatar hash."""

    @property
    def tag(self):
        """Users full Tag. eg.: `Arrg#2048`"""
        return f"{self.username}#{self.discriminator}"


class DiscordGuildMember(BaseModel):
    """
    https://discord.com/developers/docs/resources/guild#guild-member-object
    """

    user: DiscordUser
    nick: typing.Optional[str] = ""

    roles: list[str]
    """Role IDs.
    
    They come in as Ints.. but due to them represting very large numbers
    I found it safer to convert them to string instead.
    """

    joined_at: str  # ISO8601 timestamp

    avatar: typing.Optional[str] = ""


class DiscordAccessTokenResponse(typing.TypedDict):
    """
    Ref:
        https://discord.com/developers/docs/topics/oauth2#authorization-code-grant-access-token-exchange-example

    Example Content:
        >>> {
        >>>     "access_token": "<ACCESS_TOKEN>",
        >>>     "token_type": "Bearer",
        >>>     "expires_in": 604800,
        >>>     "refresh_token": "<REFRESH_TOKEN>",
        >>>     "scope": "identify"
        >>> }
    """

    access_token: str
    token_type: str  # eg.: "Bearer",
    expires_in: typing.Optional[int]
    refresh_token: typing.Optional[str]
    scope: typing.Optional[str]  # eg.: "identify"


class DiscordErrorResponse(typing.TypedDict):
    error: str
    error_description: str
