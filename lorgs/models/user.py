"""Model to describe a User of Lorrgs."""

# IMPORT THIRD PARTY LIBRARIES
import typing
import arrow
import mongoengine as me

# IMPORT LOCAL LIBRARIES
from lorgs.clients import discord
from lorgs.lib import mongoengine_arrow


LORRGS_SERVER_ID  = 885638678607708172
"""Server ID for the lorrgs discord."""


# Role IDs -> Permissions
# simple map to control who can access which modules
ROLE_PERMISSIONS = {
    "885660648510455839": ["user_reports", "mod", "admin"],  # Arrgmin
    "885660390120362024": ["user_reports", "mod"],           # Morrgerator
    "886595672525119538": ["user_reports"],                  # Investorrg
    "887397111975518288": ["user_reports"],                  # Contributorrg
    "908726333369110571": ["user_reports"],                  # User Reports Alpha Tester

    # special "role" for Liquid People
    "liquid": ["user_reports"],
}


class User(me.Document):

    meta = {
        # ignore non existing properties
        "strict": False,

        'indexes': [
            {'fields': ["discord_id", "discord_tag"]}
        ]
    }

    discord_id: int = me.IntField()

    # Discord Hame+Hash: eg.: "Arrg#2048"
    discord_tag: str = me.StringField()

    discord_avatar: str = me.StringField()

    # Role IDs
    discord_roles: list[str] = me.ListField(me.StringField(), default=[]) 

    extra_roles: list[str] = me.ListField(me.StringField(), default=[]) 

    # just for info
    last_login: arrow.Arrow = mongoengine_arrow.ArrowDateTimeField() 

    # last time the roles have been checked
    updated: arrow.Arrow = mongoengine_arrow.ArrowDateTimeField() 

    @classmethod
    def get_or_create(cls, discord_id=0, discord_tag="") -> "User":
        user = cls.objects(discord_id=discord_id).first()
        user = user or cls.objects(discord_tag=discord_tag).first()
        user = user or cls(discord_id=discord_id, discord_tag=discord_tag)
        return user  # type: ignore

    ################################
    # Properties
    #
    @property
    def name(self):
        """The Users Name only (eg.: Arrg#2048 -> Arrg)"""
        return self.discord_tag.split("#")[0]

    @property
    def discriminator(self):
        """The Users discriminator (eg.: Arrg#2048 -> 2048)"""
        return self.discord_tag.split("#")[-1]

    @property
    def roles(self):
        """All Roles the User has."""
        return list(set(self.discord_roles + self.extra_roles))

    @property
    def permissions(self) -> set[str]:
        """All Permissions the User has."""
        permissions = set()
        for role in self.roles:
            role_permissions = ROLE_PERMISSIONS.get(role, [])
            permissions.update(role_permissions)
        return permissions

    def to_dict(self):
        return {
            "id": str(self.discord_id),  # as string due to numerical issues
            "name": self.discord_tag,

            "avatar": self.discord_avatar,
            "permissions": self.permissions,

            # "last_login": self.last_login,
            "updated": self.updated.isoformat()
        }

    ################################
    # Methods
    #

    async def refresh(self) -> None:
        """Refresh the User Info from Discord."""

        # update discord roles / avatar
        member_info = await discord.get_member_info(server_id=LORRGS_SERVER_ID, user_id=self.discord_id)
        user_info = member_info.user

        self.discord_tag = user_info.tag
        self.discord_avatar = member_info.avatar or user_info.avatar or ""
        self.discord_roles = member_info.roles or []
        self.updated = arrow.utcnow()
