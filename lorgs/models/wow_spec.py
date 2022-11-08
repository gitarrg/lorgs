"""Models for Classes, Specs, Spells and Roles."""

# IMPORT STANDARD LIBRARIES
import typing

# IMPORT LOCAL LIBRARIES
from lorgs import utils
from lorgs.models.wow_actor import WowActor
from lorgs.models.wow_spell import WowSpell

if typing.TYPE_CHECKING:
    from lorgs.models.wow_role import WowRole
    from lorgs.models.wow_class import WowClass


class WowSpec(WowActor):
    """docstring for Spec"""

    def __init__(self, wow_class: "WowClass", name: str, role: "WowRole", short_name: str = "") -> None:
        super().__init__()
        self.name = name

        self.role = role
        self.role.specs.append(self)

        self.wow_class = wow_class
        self.wow_class.specs.append(self)
        self.parents = [self.wow_class]

        # Generate some names
        self.full_name = f"{self.name} {self.wow_class.name}"
        self.short_name = short_name or self.name  # to be overwritten

        # slugified names
        self.name_slug = utils.slug(self.name)
        self.full_name_slug = f"{self.wow_class.name_slug}-{self.name_slug}"

        # str: Spec Name without spaces, but still capCase.. eg.: "BeastMastery"
        self.name_slug_cap = self.name.replace(" ", "")

    def __repr__(self) -> str:
        return f"<Spec({self.full_name})>"

    def __lt__(self, other: "WowSpec") -> bool:
        def sort_key(obj: WowSpec) -> tuple["WowRole", "WowClass", str]:
            return (obj.role, obj.wow_class, obj.name)

        return sort_key(self) < sort_key(other)

    def as_dict(self) -> dict[str, typing.Any]:
        return {
            "name": self.name,
            "full_name": self.full_name,
            "full_name_slug": self.full_name_slug,
            "role": self.role.code,
            "class": {
                "name": self.wow_class.name,  # required for the WCL-Header Link
                "name_slug": self.wow_class.name_slug,
            },
        }

    ##########################
    # Methods
    #
    def add_spell(self, spell: typing.Optional[WowSpell] = None, **kwargs: typing.Any) -> WowSpell:
        kwargs.setdefault("color", self.wow_class.color)
        return super().add_spell(spell, **kwargs)

    def add_buff(self, spell: typing.Optional[WowSpell] = None, **kwargs) -> WowSpell:
        kwargs.setdefault("color", self.wow_class.color)
        return super().add_buff(spell, **kwargs)

    def add_debuff(self, spell: typing.Optional[WowSpell] = None, **kwargs) -> WowSpell:
        kwargs.setdefault("color", self.wow_class.color)
        return super().add_debuff(spell, **kwargs)

    def add_event(self, event: typing.Optional[WowSpell] = None, **kwargs: typing.Any) -> WowSpell:
        kwargs.setdefault("color", self.wow_class.color)
        return super().add_event(event, **kwargs)
