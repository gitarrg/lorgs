# IMPORT STANDARD LIBRARIES
import typing

# IMPORT THIRD PARTY LIBRARIES
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

    @classmethod
    def get_json_aliases(cls) -> dict[str, str]:
        r = {}
        for name, field in cls.__fields__.items():
            alias = field.field_info.extra.get("json_alias")
            if alias:
                r[name] = alias
        return r

    @pydantic.validator("spell_id")
    def resolve_spell_id(cls, spell_id: int) -> int:
        return WowSpell.resolve_spell_id(spell_id)

    @pydantic.root_validator(pre=True)
    def rename_fields_in(cls, data: dict[str, typing.Any]) -> dict[str, typing.Any]:
        return utils.rename_dict_keys(data, cls.get_json_aliases(), reverse=True)

    def __str__(self):
        time_fmt = utils.format_time(self.timestamp)
        return f"Cast({self.spell_id}, at={time_fmt})"

    def dict(self, **kwargs: typing.Any):
        data = super().dict(**kwargs)
        return utils.rename_dict_keys(data, self.get_json_aliases())

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
