# IMPORT STANDARD LIBRARIES
import typing

# IMPORT THIRD PARTY LIBRARIES
import pydantic

# IMPORT LOCAL LIBRARIES
from lorgs import utils
from lorgs.models.wow_spell import WowSpell

if typing.TYPE_CHECKING:
    from lorgs.clients import wcl


class Cast(pydantic.BaseModel):
    """An Instance of a Cast of a specific Spell in a Fight."""

    spell_id: int = pydantic.Field(json_alias="id")
    """ID of the spell/aura."""

    timestamp: int = pydantic.Field(json_alias="ts")
    """time the spell was cast, in milliseconds relative to the start of the fight."""

    duration: typing.Optional[int] = pydantic.Field(json_alias="d", default=None)
    """time the spell/buff was active in milliseconds."""

    event_type: str = pydantic.Field(default="cast", exclude=True)

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

    #############################

    @classmethod
    def from_report_event(cls, event: "wcl.ReportEvent") -> "Cast":
        return cls(
            spell_id=event.abilityGameID,
            timestamp=event.timestamp,
            event_type=event.type,
        )

    def __str__(self):
        time_fmt = utils.format_time(self.timestamp)
        return f"Cast({self.spell_id}, at={time_fmt})"

    def dict(self, **kwargs: typing.Any):
        data = super().dict(**kwargs)
        return utils.rename_dict_keys(data, self.get_json_aliases())

    @property
    def spell(self) -> WowSpell:
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

    @staticmethod
    def process_auras(events: list["Cast"]) -> list["Cast"]:
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

    @staticmethod
    def process_until_events(casts: list["Cast"]) -> list["Cast"]:
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
