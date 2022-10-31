
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

    timestamp: int
    """Timestamp of the Event (Milliseconds relative to the Report Start)."""

    type: typing.Union[EventDataType, str]
    """The type of Event. """

    sourceID: int

    targetID: int

    abilityGameID: int

    fight: int

    duration: int = 0
