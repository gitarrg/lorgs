# IMPORT STANDARD LIBRARIES
import typing

# IMPORT THIRD PARTY LIBRARIES
from pydantic import BaseModel

# IMPORT LOCAL LIBRARIES
from .zone import Zone
from .character_ranking import CharacterRankings


class Encounter(BaseModel):
    """A single encounter for the game.."""
    
    id: int = 0
    """The ID of the encounter."""

    name: str = ""
    """The localized name of the encounter."""

    zone: typing.Optional[Zone] = None
    """The zone that this encounter is found in."""

    characterRankings: CharacterRankings = CharacterRankings()
    """Player rankings information for a encounter."""
