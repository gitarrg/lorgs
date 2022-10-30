"""Model to describe a User of Lorrgs."""

# IMPORT THIRD PARTY LIBRARIES
import typing
from typing import List
import arrow
import mongoengine as me

# IMPORT LOCAL LIBRARIES
from lorgs import auth
from lorgs.lib import mongoengine_arrow


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


class User(me.Document):  # type: ignore

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
    discord_roles: List[str] = me.ListField(me.StringField(), default=[]) 

    extra_roles: List[str] = me.ListField(me.StringField(), default=[]) 

    # just for info
    last_login: arrow.Arrow = mongoengine_arrow.ArrowDateTimeField() 

    # last time the roles have been checked
    updated: arrow.Arrow = mongoengine_arrow.ArrowDateTimeField() 

    ################################
    # insert generated fields
    if typing.TYPE_CHECKING:
        @classmethod
        def objects(cls, **kwargs):

            class X():
                def first(self) -> typing.Optional[User]:
                    return User()
            return X()


    ################################
    # Properties
    #
    @property
    def name(self):
        return self.discord_tag.split("#")[0]

    @property
    def discriminator(self):
        return self.discord_tag.split("#")[-1]

    @property
    def roles(self):
        return list(set(self.discord_roles + self.extra_roles))

    @property
    def permissions(self) -> typing.Set[str]:
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
            "updated": int(self.updated.timestamp()) if self.updated else 0,
        }

    ################################
    # Methods
    #

    async def refresh(self):
        """Refresh the User Info from Discord."""

        # update discord roles / avatar
        member_info = await auth.get_member_info(self.discord_id)
        user_info = member_info.get("user") or {}

        # help convert old logins
        if not self.discord_tag:
            try:
                self.discord_tag = "{username}#{discriminator}".format(**user_info)
            except KeyError:
                pass

        self.discord_avatar = member_info.get("avatar") or user_info.get("avatar") or ""
        self.discord_roles = member_info.get("roles") or []
        self.updated = arrow.utcnow()
