"""Playable (and some non playble) Classes in WoW."""

# IMPORT STANDARD LIBRARIES
import typing

# IMPORT LOCAL LIBRARIES
from lorgs import utils
from lorgs.models import base
from lorgs.models.wow_spec import WowSpec
from lorgs.models.wow_spell import WowSpell


class WowClass(base.Model):
    """A playable class in wow."""

    def __init__(self, id: int, name: str, color: str = ""):

        # int: class id, mostly used for sorting
        self.id = id
        self.name = name
        self.color = color
        self.specs: list[WowSpec] = []
        self.spells: list[WowSpell] = []
        self.buffs: list[WowSpell] = []
        self.debuffs: list[WowSpell] = []

        self.name_slug_cap = self.name.replace(" ", "")
        self.name_slug = utils.slug(self.name)

        #: bool: flag for the trinkets/potions groups
        self.is_other = self.name.lower() == "other"

    def __repr__(self):
        return f"<Class(name='{self.name}')>"

    def __lt__(self, other: "WowClass") -> bool:
        return self.id < other.id

    def as_dict(self):
        return {
            "name": self.name,
            "name_slug": self.name_slug,
            "specs": [spec.full_name_slug for spec in self.specs]
        }

    ##########################
    # Methods
    #
    def add_spell(self, **kwargs: typing.Any) -> WowSpell:
        kwargs.setdefault("color", self.color)
        kwargs.setdefault("spell_type", self.name_slug)

        spell = WowSpell(**kwargs)
        self.spells.append(spell)
        return spell

    def add_buff(self, spell: typing.Optional[WowSpell] = None, **kwargs: typing.Any) -> None:

        if not spell:
            kwargs.setdefault("color", self.color)
            kwargs.setdefault("spell_type", self.name_slug)
            spell = WowSpell(**kwargs)

        self.buffs.append(spell)

    def add_debuff(self, spell: typing.Optional[WowSpell] = None, **kwargs: typing.Any) -> None:

        if not spell:
            kwargs.setdefault("color", self.color)
            kwargs.setdefault("spell_type", self.name_slug)
            spell = WowSpell(**kwargs)

        self.debuffs.append(spell)
