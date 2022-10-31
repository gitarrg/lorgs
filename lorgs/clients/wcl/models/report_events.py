
# IMPORT STANDARD LIBRARIES
import typing

# IMPORT THIRD PARTY LIBRARIES
from pydantic import BaseModel


EventDataType = typing.Literal[
    "cast",
    "damage",
    "applybuff", "removebuff",
    "applydebuff", "removedebuff",
    "resurrect",
]


class ReportEvent(BaseModel):
    """Represents a single event that occurs in the fight."""

    timestamp: int = 0
    """Timestamp of the Event (Milliseconds relative to the Report Start)."""

    type: typing.Union[EventDataType, str] = ""
    """The type of Event. """

    sourceID: int = 0

    targetID: int = 0

    abilityGameID: int = 0

    fight: int = 0

    duration: int = 0
