"""Models a Covenant in the Game."""

# IMPORT LOCAL LIBRARIES
from lorgs import utils
from lorgs.models import base


class WowCovenant(base.Model):
    """Datacontainer for Covenants in the Game.

    Nightfae, Necrolord, Ventyr and Kyrian.

    """
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name
        self.name_slug = utils.slug(self.name)

    def __repr__(self):
        return f"<Covenant({self.name})>"
