
# IMPORT THIRD PARTY LIBRARIES
import mongoengine as me

# IMPORT LOCAL LIBRARIES
from lorgs import utils
from lorgs.models.wow_spell import WowSpell


class Cast(me.EmbeddedDocument):
    """An Instance of a Cast of a spezific Spell in a Fight."""

    timestamp: int = me.IntField()
    spell_id: int = me.IntField()
    duration: int = me.IntField()

    def __str__(self):
        time_fmt = utils.format_time(self.timestamp)
        return f"Cast({self.spell_id}, at={time_fmt})"

    def as_dict(self):
        dict = {
            "ts": self.timestamp,
            "id": self.spell_id,
        }
        if self.duration:
            dict["d"] = self.duration
        return dict

    ##########################
    # Attributes
    #
    @property
    def spell(self) -> WowSpell:
        return WowSpell.get(spell_id=self.spell_id)

    @property
    def end_time(self):
        return self.timestamp + (self.duration * 1000)

    @end_time.setter
    def end_time(self, value):
        self.duration = (value - self.timestamp) / 1000