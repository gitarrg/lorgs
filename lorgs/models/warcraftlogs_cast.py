from __future__ import annotations

# IMPORT STANDARD LIBRARIES
from typing import TYPE_CHECKING

# IMPORT THIRD PARTY LIBRARIES
import pydantic

# IMPORT LOCAL LIBRARIES
from lorgs import utils
from lorgs.models import base
from lorgs.models.wow_spell import WowSpell


if TYPE_CHECKING:
    from lorgs.clients import wcl


class Cast(base.BaseModel):
    """An Instance of a Cast of a specific Spell in a Fight."""

    spell_id: int = pydantic.Field(alias="id")
    """ID of the spell/aura."""

    timestamp: int = pydantic.Field(alias="ts")
    """time the spell was cast, in milliseconds relative to the start of the fight."""

    duration: int | None = pydantic.Field(default=None, alias="d")
    """time the spell/buff was active in milliseconds."""

    event_type: str = pydantic.Field(default="cast", exclude=True)

    model_config = pydantic.ConfigDict(populate_by_name=True)

    #############################

    @classmethod
    def from_report_event(cls, event: "wcl.ReportEvent") -> "Cast":
        spell_id = WowSpell.resolve_spell_id(event.abilityGameID)
        return cls(
            spell_id=spell_id,
            timestamp=event.timestamp,
            event_type=event.type,
        )

    def __str__(self):
        time_fmt = utils.format_time(self.timestamp)
        return f"Cast(id={self.spell_id}, ts={time_fmt})"

    @property
    def spell(self) -> WowSpell | None:
        return WowSpell.get(spell_id=self.spell_id)

    def get_duration(self) -> int:
        if self.duration:
            return self.duration

        if self.spell:
            return self.spell.duration * 1000

        return 0

    ############################################################################
    # Cast Processing functions
    #
    def convert_to_start_event(self) -> None:
        """Convert this Cast into a start event.

        eg.: Convert from "remove debuff" to "apply debuff"
        and automatically shift the timestamp based on the spell default duration
        """
        self.event_type = self.event_type.replace("remove", "apply")
        self.timestamp -= self.get_duration()


def process_auras(events: list[Cast]) -> list[Cast]:
    """Calculate Aura Durations from "applybuff" to "applydebuff".

    Also converts "removebuff" events without matching "apply"
    eg.: a "removebuff" from an Aura that got applied prepull

    """
    # spell id --> application event
    active_buffs: dict[int, Cast] = {}

    for event in events:
        spell_id = event.spell_id

        # track the applications (pref initial)
        if event.event_type in ("applybuff", "applydebuff"):
            # Buffs with predefined/fixed duration need to custom logic.
            # we can simply pass over them here
            if event.get_duration() > 0:
                continue

            if event.spell_id in active_buffs:  # this is already tracked
                event.spell_id = -1
                continue

            active_buffs[spell_id] = event
            continue

        if event.event_type in ("removebuff", "removedebuff"):
            start_event = active_buffs.get(spell_id)

            # calc dynamic duration from start -> end
            if start_event:
                start_event.duration = event.timestamp - start_event.timestamp
                active_buffs.pop(event.spell_id)
                event.spell_id = -1
            else:
                # Automatically create start event
                event.convert_to_start_event()

    return [event for event in events if event.spell_id >= 0]


def process_until_events(casts: list[Cast]) -> list[Cast]:
    """Dynamically set the duration from the corresponding "until"-event."""

    for cast in casts:
        spell = cast.spell
        if not (spell and spell.until):
            continue

        # find valid "until"-events
        end_events = [e for e in casts if (e.timestamp > cast.timestamp) and (e.spell_id == spell.until.spell_id)]
        if not end_events:
            continue

        end_event = end_events[0]
        end_event.spell_id = -1  # flag for filtering
        cast.duration = end_event.timestamp - cast.timestamp

    return [c for c in casts if c.spell_id > 0]
