
# IMPORT THIRD PARTY LIBRARIES
from email.policy import default
import typing
import mongoengine as me

# IMPORT LOCAL LIBRARIES
from lorgs import utils
from lorgs.models.wow_spell import WowSpell


class Cast(me.EmbeddedDocument):
    """An Instance of a Cast of a specific Spell in a Fight."""

    spell_id: int = me.IntField()
    """ID of the spell/aura."""

    timestamp: int = me.IntField()
    """time the spell was cast, in milliseconds relative to the start of the fight."""

    duration: int = me.IntField()
    """time the spell/buff was active in milliseconds."""

    def __init__(self, spell_id: int, timestamp: int, duration=0, event_type: str = "cast", **kwargs):
        super().__init__(spell_id=spell_id, timestamp=timestamp, duration=duration)
        self.spell_id = WowSpell.resolve_spell_id(self.spell_id)
        self.event_type = event_type

    def __str__(self):
        time_fmt = utils.format_time(self.timestamp)
        return f"Cast({self.spell_id}, at={time_fmt})"

    def as_dict(self) -> dict[str, typing.Any]:
        info = {
            "ts": self.timestamp,
            "id": self.spell_id,
        }
        if self.duration_:
            info["d"] = self.duration_
        return info

    ##########################
    # Attributes
    #
    @property
    def spell(self) -> WowSpell:
        return WowSpell.get(spell_id=self.spell_id)

    # @property
    # def end_time(self):
    #     """"Time the Spell/Aura faded. (relative to Fight Start, in milliseconds)."""
    #     return self.timestamp + self.duration

    # @end_time.setter
    # def end_time(self, value: int) -> None:
    #     self.duration = (value - self.timestamp)

    def get_duration(self) -> int:
        """TODO: use a property + setter."""
        if self.duration:
            return self.duration

        if self.spell:
            return self.spell.duration * 1000
        
        return 0

    def convert_to_start_event(self) -> None:
        """Convert this Cast into a start event.

        eg.: Convert from "remove debuff" to "apply debuff"
        and automatically shift the timestamp based on the spell default duration
        """
        self.event_type = self.event_type.replace("remove", "apply")
        self.timestamp -= self.get_duration()
