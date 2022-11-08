"""Playable (and some non playble) Classes in WoW."""

# IMPORT STANDARD LIBRARIES
import typing

# IMPORT LOCAL LIBRARIES
from lorgs import utils
from lorgs.models.wow_actor import WowActor
from lorgs.models.wow_spec import WowSpec
from lorgs.models.wow_spell import WowSpell


class WowClass(WowActor):
    """A playable class in wow."""

    def __init__(self, id: int, name: str, color: str = "") -> None:
        super().__init__()

        # int: class id, mostly used for sorting
        self.id = id
        self.name = name
        self.color = color
        self.specs: list[WowSpec] = []

        self.name_slug_cap = self.name.replace(" ", "")
        self.name_slug = utils.slug(self.name)

        #: bool: flag for the trinkets/potions groups
        self.is_other = self.name.lower() == "other"

    def __repr__(self) -> str:
        return f"<Class(name='{self.name}')>"

    def __lt__(self, other: "WowClass") -> bool:
        return self.id < other.id

    def as_dict(self) -> dict[str, typing.Any]:
        return {"name": self.name, "name_slug": self.name_slug, "specs": [spec.full_name_slug for spec in self.specs]}

    ##########################
    # Methods
    #
    def add_spell(self, spell: typing.Optional[WowSpell] = None, **kwargs: typing.Any) -> WowSpell:
        kwargs.setdefault("color", self.color)
        return super().add_spell(spell, **kwargs)

    def add_buff(self, spell: typing.Optional[WowSpell] = None, **kwargs: typing.Any) -> WowSpell:
        kwargs.setdefault("color", self.color)
        return super().add_buff(spell, **kwargs)

    def add_debuff(self, spell: typing.Optional[WowSpell] = None, **kwargs: typing.Any) -> WowSpell:
        kwargs.setdefault("color", self.color)
        return super().add_debuff(spell, **kwargs)

    def add_event(self, event: typing.Optional[WowSpell] = None, **kwargs: typing.Any) -> WowSpell:
        kwargs.setdefault("color", self.color)
        return super().add_event(event, **kwargs)
