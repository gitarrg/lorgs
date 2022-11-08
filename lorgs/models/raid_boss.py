"""Defines an Encounter/RaidBoss in the Game.."""

# IMPORT STANDARD LIBRARIES
import typing

# IMPORT LOCAL LIBRARIES
from lorgs import utils
from lorgs.models.wow_actor import WowActor
from lorgs.models.wow_spell import WowSpell


class RaidBoss(WowActor):
    """A raid boss in the Game."""

    def __init__(self, id: int, name: str, nick: str = ""):
        """Initialise a new Raid Boss

        Args:
            id (int): Encounter ID
            name (str): Nice Name
            nick (str, optional): Nick Name. Defaults to `name`.
        """
        super().__init__()

        self.id = id
        """The Encounter ID."""

        self.full_name = name
        """Full Name of the Boss (eg.: "Halondrus the Reclaimer")."""

        self.name = nick or name
        """Short commonlty used Nickname. eg.: "Halondrus"."""

        self.full_name_slug = utils.slug(self.full_name, space="-")
        """Complete Name slugified. eg.: `"halondrus-the-reclaimer"`."""

        # alias
        self.add_cast = self.add_spell

    def __repr__(self):
        return f"<RaidBoss(id={self.id} name={self.name})>"

    def as_dict(self) -> dict[str, typing.Any]:
        return {
            "id": self.id,
            "name": self.name,
            "full_name": self.full_name,
            "full_name_slug": self.full_name_slug,
        }

    @property
    def full_name_slug(self):
        """Complete Name slugified. eg.: `"halondrus-the-reclaimer"`."""
        return utils.slug(self.full_name, space="-")

    # @property
    # def icon(self):
    #     """Relative path to the Boss Icon."""
    #     return f"bosses/{self.zone.name_slug}/{self.full_name_slug}.jpg"

    @property
    def all_abilities(self):
        """Complete List of all Spells, Buffs and other Events."""
        return self.spells + self.buffs + self.event_spells

    ##########################
    # Methods
    #
    def add_cast(self, **kwargs: typing.Any) -> WowSpell:
        kwargs.setdefault("spell_type", self.full_name_slug)
        spell = WowSpell(**kwargs)

        self.spells.append(spell)
        return spell

    def add_buff(self, spell_id: int, **kwargs: typing.Any) -> WowSpell:
        kwargs.setdefault("spell_type", self.full_name_slug)
        spell = WowSpell(spell_id=spell_id, **kwargs)

        self.buffs.append(spell)
        return spell

    def add_event(self, **kwargs: typing.Any): # event_type, spell_id, name: str, icon: str, duration: int = 0):
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

        # spell.specs = [self]
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

    def preprocess_query_results(self, **query_results: typing.Any):

        # TODO:
        #   not 100% sure what this was supposed to do.
        #   I think its the custom "unit-event"-logic
        #   Might need some time/rework
        return query_results

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
