
# IMPORT THIRD PARTY LIBRARIES
import mongoengine as me

# IMPORT LOCAL LIBRARIES
from lorgs import utils
from lorgs.models.wow_spell import WowSpell


class Cast(me.EmbeddedDocument):
    """An Instance of a Cast of a specific Spell in a Fight."""

    # ID of the spell
    spell_id: int = me.IntField()

    # time the spell was cast, in milliseconds relativ to the start of the fight
    timestamp: int = me.IntField()

    # time the spell/buff was active in milliseconds
    duration: int = me.IntField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # int: track the number
        self.stacks = 0

    def __str__(self):
        time_fmt = utils.format_time(self.timestamp)
        return f"Cast({self.spell_id}, at={time_fmt})"

    def as_dict(self):
        info = {
            "ts": self.timestamp,
            "id": self.spell_id,
        }
        if self.duration:
            info["d"] = self.duration
        return info

    ##########################
    # Attributes
    #
    @property
    def spell(self) -> WowSpell:
        return WowSpell.get(spell_id=self.spell_id)

    @property
    def end_time(self):
        return self.timestamp + self.duration

    @end_time.setter
    def end_time(self, value: int):
        self.duration = (value - self.timestamp)
