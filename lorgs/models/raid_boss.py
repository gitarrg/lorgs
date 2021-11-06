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
        self.event_spells: typing.List["WowSpell"] = []

    def __repr__(self):
        return f"<RaidBoss(id={self.id} name={self.name})>"

    def as_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "full_name": self.full_name,
            "full_name_slug": self.full_name_slug,
        }

    @property
    def all_abilities(self):
        return self.spells + self.buffs + self.event_spells

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

        # dedicated "stop" event, for events with non static timers.. eg: intermissions
        end_event = kwargs.get("until", {})
        if end_event:
            self.events.append(end_event)

        # spell instance used for UI things
        kwargs.setdefault("spell_type", self.full_name_slug)
        spell = WowSpell(**kwargs)

        spell.specs = [self]
        self.event_spells.append(spell)

    ##########################
    # Methods
    #
    def get_events_query(self) -> str:

        filters = []

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


    def preprocess_query_results(self, query_results):

        casts = utils.get_nested_value(query_results, "report", "events", "data") or []
        events_by_id = {event.get("spell_id"): event for event in self.events}

        def get_duration(event_data, cast_data, casts):
            """
                event_data: the event we are checking
                cast_data: the current cast of that event
                casts: list of all casts
            """
            until = event_data.get("until")
            if not until:
                return

            until_id = until.get("spell_id")
            timestamp = cast_data.get("timestamp")

            end_events = [
                cast for cast in casts if
                cast.get("abilityGameID") == until_id and cast.get("timestamp") > timestamp
            ]
            if not end_events:
                return
            end_event = end_events[0]
            end_event["remove"] = True
            cast_data["duration"] = end_event.get("timestamp") - cast_data.get("timestamp")


        for cast_data  in casts:
            spell_id = cast_data.get("abilityGameID")

            # check if this is a custom event
            event_data = events_by_id.get(spell_id)
            if not event_data:
                continue

            get_duration(event_data, cast_data, casts)


        casts = [cast for cast in casts if not cast.get("remove")]

        query_results["report"]["events"]["data"] = casts
        return query_results

