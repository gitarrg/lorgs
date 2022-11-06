# IMPORT THIRD PARTY LIBRARIES
import typing
import pydantic

# IMPORT LOCAL LIBRARIES
from lorgs import utils
from lorgs.models.wow_spell import WowSpell


class Cast(pydantic.BaseModel):
    """An Instance of a Cast of a specific Spell in a Fight."""

    spell_id: int = pydantic.Field(json_alias="id")
    """ID of the spell/aura."""

    # timestamp: int
    timestamp: int = pydantic.Field(json_alias="ts")
    """time the spell was cast, in milliseconds relative to the start of the fight."""

    duration: typing.Optional[int] = pydantic.Field(json_alias="d", default=None)
    """time the spell/buff was active in milliseconds."""

    event_type: str = pydantic.Field(default="cast", exclude=True)

    ######################
    # Validators

    @pydantic.validator("spell_id")
    def resolve_spell_id(cls, spell_id: int):
        return WowSpell.resolve_spell_id(spell_id)

    @pydantic.root_validator(pre=True)
    def rename_fields_in(cls, data):
        for name, field in cls.__fields__.items():
            alias = field.field_info.extra.get("json_alias")
            if alias:
                data[name] = data.get(name) or data.get(alias)
        return data

    def __str__(self):
        time_fmt = utils.format_time(self.timestamp)
        return f"Cast({self.spell_id}, at={time_fmt})"

    def dict(self, **kwargs: typing.Any):
        data = super().dict(**kwargs)
        # apply json aliases
        for name, field in self.__fields__.items():
            alias = field.field_info.extra.get("json_alias")
            if alias:
                data[alias] = data.get(alias) or data.get(name)
        return data

    ##########################
    # Attributes
    #
    @property
    def spell(self) -> WowSpell:
        return WowSpell.get(spell_id=self.spell_id)

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
