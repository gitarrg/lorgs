"""Model to describe a User of Lorrgs."""

# IMPORT THIRD PARTY LIBRARIES
import arrow
import mongoengine as me

# IMPORT LOCAL LIBRARIES
from lorgs.lib import mongoengine_arrow


class User(me.EmbeddedDocument):

    meta = {
        # ignore non existing properties
        "strict": False,

        'indexes': [
            {'fields': ['discord_tag']}
        ]
    }

    discord_id: int = me.IntField(primary_key=True)

    # Discord Hame+Hash: eg.: "Arrg#2048"
    discord_tag: int = me.StringField()

    # Role Names: eg.: ["Admin", "Beta Tester", "Patreon L2"]
    roles = me.ListField(me.StringField())

    # just for info
    last_login: arrow.Arrow = mongoengine_arrow.ArrowDateTimeField()

    # last time the roles have been checked
    updated: arrow.Arrow = mongoengine_arrow.ArrowDateTimeField()

