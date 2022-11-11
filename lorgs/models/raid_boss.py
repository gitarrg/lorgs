"""Defines an Encounter/RaidBoss in the Game.."""

from __future__ import annotations

# IMPORT STANDARD LIBRARIES
import typing

# IMPORT LOCAL LIBRARIES
from lorgs import utils
from lorgs.models.wow_actor import WowActor
from lorgs.models.wow_spell import WowSpell


class RaidBoss(WowActor):
    """A raid boss in the Game."""

    id: int
    """The Encounter ID."""

    name: str = ""
    """Full Name of the Boss (eg.: "Halondrus the Reclaimer")."""

    nick: str = ""
    """Short commonlty used Nickname. eg.: "Halondrus"."""

    def __repr__(self):
        return f"<RaidBoss(id={self.id} name={self.name})>"

    # alias
    def add_cast(self, *args, **kwargs) -> WowSpell:
        return self.add_spell(*args, **kwargs)

    @property
    def name_slug(self) -> str:
        """Complete Name slugified. eg.: `"halondrus-the-reclaimer"`."""
        return utils.slug(self.name, space="-")

    # Alias to maintain the Actor-Interface
    @property
    def full_name_slug(self) -> str:
        return self.name_slug

    def as_dict(self) -> dict[str, typing.Any]:
        return {
            "id": self.id,
            # renames to match the "Actor"-Interface
            "name": self.nick or self.name,
            "full_name": self.name,
            "full_name_slug": self.name_slug,
        }
