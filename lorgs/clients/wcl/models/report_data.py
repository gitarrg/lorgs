"""Data we receive from WCL under the reportData."""
import datetime
import typing

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

    type: typing.Union[EventDataType, str]
    """The type of Event. """
    sourceID: int
    targetID: int
    abilityGameID: int
    fight: int
    duration: int = 0


class ReportEventPaginator(BaseModel):
    """The ReportEventPaginator represents a paginated list of report events."""

    data: typing.List[ReportEvent] = []
    """The list of events obtained."""

    nextPageTimestamp: float = 0
    """A timestamp to pass in as the start time when fetching the next page of data."""


class Report(BaseModel):
    """A single report uploaded by a player to a guild or personal logs."""

    code: typing.Optional[str]
    """The report code, a unique value used to identify the report."""

    title: typing.Optional[str]
    """A title for the report."""

    endTime: typing.Optional[datetime.datetime]
    """The end time of the report. Representing the timestamp of the last event contained in the report."""

    visibility: typing.Optional[typing.Literal["public", "private", "unlisted"]] = "public"
    """The visibility level of the report."""

    events: ReportEventPaginator = ReportEventPaginator()
    """A set of report events, filterable via arguments like type, source, target, ability, etc."""


class ReportData(BaseModel):
    """The ReportData object enables the retrieval of single reports or filtered collections of reports."""

    report: Report
