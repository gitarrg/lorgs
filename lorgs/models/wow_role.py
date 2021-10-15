"""Models for a Role in the Game."""

# IMPORT LOCAL LIBRARIES
from lorgs.models import base


class WowRole(base.Model):
    """A role like Tank, Healer, DPS."""

    def __init__(self, id: int, name: str, code=""):
        self.id = id  #used for sorting
        self.name = name
        self.code = code or name.lower()
        self.specs = []

        # still used on the flask index page
        self.icon = f"roles/{self.code}.jpg"

    def __repr__(self):
        return f"<Role({self.name})>"

    def __str__(self):
        return self.code

    def __lt__(self, other):
        return self.id < other.id

    # @property
    # def specs(self):
    #     from lorgs.models.wow_spec import WowSpec # circular import as WowSpec also needs WowRole
    #     return [spec for spec in WowSpec.all if spec.role == self]

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
