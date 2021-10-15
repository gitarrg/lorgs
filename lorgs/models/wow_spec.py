"""Models for Classes, Specs, Spells and Roles."""

# IMPORT STANDARD LIBRARIES
from collections import defaultdict
import typing

# IMPORT LOCAL LIBRARIES
from lorgs import utils
from lorgs.models import base
from lorgs.models.wow_spell import WowSpell

if typing.TYPE_CHECKING:
    from lorgs.models.wow_role import WowRole
    from lorgs.models.wow_class import WowClass


def spells_by_type(spells: typing.List[WowSpell]) -> dict:
    """Groups the given spells by their spell_type.

    Note:
        only returns the IDs (because thats the only thing I need now)
    """
    groups = defaultdict(list)

    for spell in spells:
        groups[spell.spell_type] += [spell]

    return dict(groups)


def spell_ids(spells) -> typing.List[int]:
    """Converts a list of Spells to their spell_ids."""
    return [spell.spell_id for spell in spells]



class WowSpec(base.Model):
    """docstring for Spec"""

    def __init__(self, wow_class: "WowClass", name: str, role: "WowRole", short_name: str = ""):
        super().__init__()
        self.name = name

        self.spells = []

        self.role = role
        self.role.specs.append(self)

        self.wow_class = wow_class
        self.wow_class.specs.append(self)

        # Generate some names
        self.full_name = f"{self.name} {self.wow_class.name}"
        self.short_name = short_name or self.name # to be overwritten

        # slugified names
        self.name_slug = utils.slug(self.name)
        self.full_name_slug = f"{self.wow_class.name_slug}-{self.name_slug}"

        # str: Spec Name without spaces, but still capCase.. eg.: "BeastMastery"
        self.name_slug_cap = self.name.replace(" ", "")

        # still used on the flask index page
        self.icon = f"specs/{self.full_name_slug}.jpg"

    def __repr__(self):
        return f"<Spec({self.full_name})>"

    def __lt__(self, other):

        def sort_key(obj):
            return (obj.role, obj.wow_class, obj.name)

        return sort_key(self) < sort_key(other)

    def as_dict(self, **kwargs):

        data = {
            "name": self.name,
            "full_name": self.full_name,
            "full_name_slug": self.full_name_slug,
            "role": self.role.code,
            "class": {
                "name": self.wow_class.name,  # required for the WCL-Header Link
                "name_slug": self.wow_class.name_slug,
            }
        }

        if kwargs.get("spells"):
            spell_groups = spells_by_type(self.spells)
            data["spells"] = {group: spell_ids(spells) for group, spells in spell_groups.items()}

        return data

    ##########################
    # Methods
    #
    def add_spell(self, **kwargs):

        kwargs.setdefault("color", self.wow_class.color)
        kwargs.setdefault("spell_type", self.full_name_slug)

        spell = WowSpell(**kwargs)
        spell.specs.append(self)
        self.spells.append(spell)  # Important to keep a ref in memory

        return spell
