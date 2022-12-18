"""Models for a Role in the Game."""
from __future__ import annotations

# IMPORT STANDARD LIBRARIES
import typing

# IMPORT LOCAL LIBRARIES
from lorgs.models import base


if typing.TYPE_CHECKING:
    from lorgs.models.wow_spec import WowSpec


class WowRole(base.MemoryModel):
    """A role like Tank, Healer, DPS."""

    id: int  # used for sorting

    name: str
    """Full Name of the role. eg.: "Healer"."""

    code: str
    """Lowercase short Version. eg.: `tank`, `heal`, `mdps` or `rdps`."""

    @property
    def specs(self) -> list["WowSpec"]:
        from lorgs.models.wow_spec import WowSpec

        return [spec for spec in WowSpec.list() if spec.role == self]

    def __lt__(self, other: "WowRole") -> bool:
        return self.id < other.id

    def as_dict(self) -> dict[str, typing.Any]:
        return {
            "id": self.id,
            "name": self.name,
            "code": self.code,
            "specs": [spec.full_name_slug for spec in self.specs],
        }

    @property
    def metric(self) -> str:
        """str: the preferred metric. aka: dps for all. hps for healers."""
        return "hps" if self.code == "heal" else "dps"
