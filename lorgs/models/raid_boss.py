"""Defines an Encounter/RaidBoss in the Game.."""

# IMPORT STANDARD LIBRARIES
import typing

# IMPORT LOCAL LIBRARIES
from lorgs import utils
from lorgs.models.wow_actor import WowActor


class RaidBoss(WowActor):
    """A raid boss in the Game."""

    def __init__(self, id: int, name: str, nick: str = ""):
        """Initialise a new Raid Boss

        Args:
            id (int): Encounter ID
            name (str): Nice Name
            nick (str, optional): Nick Name. Defaults to `name`.
        """
        super().__init__()

        self.id = id
        """The Encounter ID."""

        self.full_name = name
        """Full Name of the Boss (eg.: "Halondrus the Reclaimer")."""

        self.name = nick or name
        """Short commonlty used Nickname. eg.: "Halondrus"."""

        self.full_name_slug = utils.slug(self.full_name, space="-")
        """Complete Name slugified. eg.: `"halondrus-the-reclaimer"`."""

        # alias
        self.add_cast = self.add_spell

    def __repr__(self):
        return f"<RaidBoss(id={self.id} name={self.name})>"

    def as_dict(self) -> dict[str, typing.Any]:
        return {
            "id": self.id,
            "name": self.name,
            "full_name": self.full_name,
            "full_name_slug": self.full_name_slug,
        }
