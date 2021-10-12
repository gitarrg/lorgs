"""Models for Raids and RaidBosses."""
# pylint: disable=too-few-public-methods

# IMPORT LOCAL LIBRARIES
from lorgs import utils
from lorgs.models import base

from lorgs.models.specs import WowSpell


class RaidZone(base.Model):
    """A raid zone in the Game."""

    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.bosses = []

        self.name_slug = utils.slug(self.name, space="-")

    def __repr__(self):
        return f"<RaidZone(id={self.id} name={self.name})>"

    def as_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "bosses": [boss.as_dict() for boss in self.bosses]
        }

    def add_boss(self, **kwargs):
        boss = RaidBoss(zone=self, **kwargs)
        self.bosses.append(boss)
        return boss


class RaidBoss(base.Model):
    """A raid boss in the Game."""

    wow_class = {
        "name": "Raid Boss",
        "name_slug": "boss",
    }

    def __init__(self, zone, id, name, nick=""):
        self.id = id
        self.zone = zone
        self.name = nick or name
        self.full_name = name
        self.visible = True # todo: is this used anywhere?

        self.name_slug = utils.slug(self.name, space="-")
        self.full_name_slug = utils.slug(self.full_name, space="-")
        self.icon = f"bosses/{self.zone.name_slug}/{self.full_name_slug}.jpg"

        # spells or buffs to track
        self.events = []

        # we track them as "spells" for now
        self.spells = []

        # alias to match the Spec Interface
        self.role = "boss"

    def __repr__(self):
        return f"<RaidBoss(id={self.id} name={self.name})>"

    def as_dict(self):
        return {
            "id": self.id,
            "role": self.role,
            "name": self.name,
            "name_slug": self.name_slug,
            "full_name": self.full_name,
            "full_name_slug": self.full_name_slug,
            "class": "boss",
        }

    ##########################
    # Methods
    #
    def add_event(self, **kwargs): # event_type, spell_id, name: str, icon: str, duration: int = 0):
        kwargs.setdefault("event_type", "cast")

        # track the event (for query)
        self.events.append(kwargs)

        # auto duration (mostly for boss buffs/debuffs)
        if kwargs.get("duration") == "auto":
            kwargs.pop("duration")

            kwargs["until"] = {}
            if kwargs.get("event_type") == "applybuff":
                kwargs["until"]["event_type"] = "removebuff"
            if kwargs.get("event_type") == "applydebuff":
                kwargs["until"]["event_type"] = "removedebuff"
            if kwargs["until"]:
                kwargs["until"]["spell_id"] = kwargs.get("spell_id", 0)

        # dedicated "stop" event, for events with non static timers.. eg: intermissions
        end_event = kwargs.get("until", {})
        if end_event:
            self.events.append(end_event)

        # spell instance used for UI things
        kwargs.setdefault("spell_type", "boss")
        spell = WowSpell(**kwargs)

        spell.specs = [self]
        self.spells.append(spell)
