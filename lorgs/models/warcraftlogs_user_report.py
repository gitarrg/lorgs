"""Classes/Functions to manage Reports injected through user interaction."""

# IMPORT STANDARD LIBRARIES
from datetime import datetime
import typing

# IMPORT LOCAL LIBRARIES
from lorgs.lib import s3_store
from lorgs.models.warcraftlogs_report import Report


class UserReport(Report, s3_store.BaseModel):
    """A single report loaded via the custom reports module."""

    # datetime: timetamp of last update
    updated: datetime = datetime.min

    # Config
    key_fmt: typing.ClassVar[str] = "{report_id}"

    ################################
    # Properties
    #
    @property
    def is_loaded(self) -> bool:
        return bool(self.fights)

    ################################
    # Methods
    #
    def save(self, *args: typing.Any, **kwargs: typing.Any) -> None:  # pylint: disable=arguments-differ
        """Update the timestamp and Save the Report."""
        self.updated = datetime.utcnow()
        return super().save(*args, **kwargs)
