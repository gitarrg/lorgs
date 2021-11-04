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
        self.events: typing.List[typing.Dict[str, str]] = []

        # we track them as "spells" for now
        self.spells: typing.List["WowSpell"] = []
        self.buffs: typing.List["WowSpell"] = []
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

    def add_cast(self, **kwargs) -> WowSpell:
        kwargs.setdefault("spell_type", self.full_name_slug)
        spell = WowSpell(**kwargs)

        self.spells.append(spell)
        return spell

    def add_buff(self, spell_id, **kwargs) -> WowSpell:

        kwargs.setdefault("spell_type", self.full_name_slug)
        spell = WowSpell(spell_id=spell_id, **kwargs)

        self.buffs.append(spell)
        return spell

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

    ##########################
    # Methods
    #
    def get_sub_query(self, filters=None) -> str:
        raise ValueError("Deprecated")
        filters = filters or []

        for event in self.events:

            # get all event parts
            parts = []
            if event.get("event_type"):
                parts.append("type='{event_type}'")
            if event.get("spell_id"):
                parts.append("ability.id={spell_id}")
            if event.get("extra_filter"):
                parts.append("{extra_filter}")

            # combine filter
            event_filter = " and ".join(parts)
            event_filter = f"({event_filter})"
            event_filter = event_filter.format(**event)

            # add filter to list
            filters.append(event_filter)

        return " or ".join(filters)
