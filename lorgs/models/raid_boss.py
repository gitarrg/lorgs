"""Defines an Encounter/RaidBoss in the Game.."""

# IMPORT STANDARD LIBRARIES
import typing

# IMPORT LOCAL LIBRARIES
from lorgs import utils
from lorgs.models import base
from lorgs.models.wow_spell import WowSpell

if typing.TYPE_CHECKING:
    from lorgs.models.raid_zone import RaidZone


class RaidBoss(base.Model):
    """A raid boss in the Game."""

    def __init__(self, zone: "RaidZone", id: int, name: str, nick=""):
        self.id = id
        self.zone = zone
        self.name = nick or name
        self.full_name = name

        self.full_name_slug = utils.slug(self.full_name, space="-")
        self.icon = f"bosses/{self.zone.name_slug}/{self.full_name_slug}.jpg"

        # spells or buffs to track
        self.events = []

        # we track them as "spells" for now
        self.spells: typing.List["WowSpell"] = []

        # self.buffs: WowSpell[] = []

        # alias to match the Spec Interface
        # self.role = "boss"

    def __repr__(self):
        return f"<RaidBoss(id={self.id} name={self.name})>"

    def as_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "full_name": self.full_name,
            "full_name_slug": self.full_name_slug,
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
        kwargs.setdefault("spell_type", self.full_name_slug)
        spell = WowSpell(**kwargs)

        spell.specs = [self]
        self.spells.append(spell)
