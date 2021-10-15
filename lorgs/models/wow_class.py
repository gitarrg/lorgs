"""The Reason why all these classes are prefixes with "wow"."""

# IMPORT LOCAL LIBRARIES
from lorgs import utils
from lorgs.models import base


class WowClass(base.Model):
    """A playable class in wow."""

    def __init__(self, id: int, name: str, color: str = ""):

        # int: class id, mostly used for sorting
        self.id = id  # pylint: disable=invalid-name
        self.name = name
        self.color = color
        self.specs = []

        self.name_slug_cap = self.name.replace(" ", "")
        self.name_slug = utils.slug(self.name)

        #: bool: flag for the trinkets/potions groups
        self.is_other = self.name.lower() == "other"

    def __repr__(self):
        return f"<Class(name='{self.name}')>"

    def __lt__(self, other) -> bool:
        return self.id < other.id

    def as_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "name_slug": self.name_slug,
        }

    def add_spell(self, **kwargs):
        kwargs.setdefault("color", self.color)
        for spec in self.specs:
            spec.add_spell(**kwargs)
