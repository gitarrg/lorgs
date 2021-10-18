"""Models for a Role in the Game."""

# IMPORT STANDARD LIBRARIES
import typing

# IMPORT LOCAL LIBRARIES
from lorgs.models import base

if typing.TYPE_CHECKING:
    from lorgs.models.wow_spec import WowSpec


class WowRole(base.Model):
    """A role like Tank, Healer, DPS."""

    def __init__(self, id: int, name: str, code: str = ""):
        self.id = id  #used for sorting
        self.name = name
        self.code = code or name.lower()
        self.specs: typing.List["WowSpec"] = []

    def __repr__(self):
        return f"<Role({self.name})>"

    def __str__(self):
        return self.code

    def __lt__(self, other: "WowRole"):
        return self.id < other.id

    def as_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "code": self.code,
            "specs": [spec.full_name_slug for spec in self.specs]
        }

    @property
    def metric(self):
        """str: the preferred metric. aka: dps for all. hps for healers."""
        return "hps" if self.code == "heal" else "dps"
