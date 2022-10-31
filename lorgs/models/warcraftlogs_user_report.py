"""Classes/Functions to manage Reports injected through user interaction."""

# IMPORT STANDARD LIBRARIES
import typing

# IMPORT THIRD PARTY LIBRARIES
import arrow
import mongoengine as me

# IMPORT LOCAL LIBRARIES
from lorgs.logger import logger
from lorgs.lib import mongoengine_arrow
from lorgs.models import warcraftlogs_report


# expire time for the tasks (2 weeks)
TTL = 60 * 60 * 24 * 7 * 2


class UserReport(me.Document):
    """Shallow Wrapper around a `warcraftlogs_report.Report`.

    Most things should be managed via the Report Instance on: `self.report`

    """

    report_id: str = me.StringField(primary_key=True)

    # datetime: timetamp of last update
    updated: arrow.Arrow = mongoengine_arrow.ArrowDateTimeField(default=arrow.utcnow)

    # the wrapped report object
    report: warcraftlogs_report.Report = me.EmbeddedDocumentField(warcraftlogs_report.Report)

    meta = {
        'indexes': [
            {'fields': ['updated'], 'expireAfterSeconds': TTL}
        ]
    }

    @classmethod
    def from_report_id(cls, report_id: str, create=False) -> typing.Union["UserReport", None]:
        """Need to split it, as otherwise the creation with nested parm does;t work"""
        user_report: "UserReport" = cls.objects(report_id=report_id).first()  # pylint: disable=no-member
        if user_report:
            return user_report

        if not create:
            return None

        user_report = cls(report_id=report_id)
        user_report.report = warcraftlogs_report.Report(report_id=report_id)
        return user_report

    ################################
    # Properties
    #
    def as_dict(self) -> dict[str, typing.Any]:
        info = self.report.as_dict()
        info["updated"] = int(self.updated.timestamp())
        return info

    @property
    def is_loaded(self):
        return bool(self.report.fights)

    ################################
    # Methods
    #
    def save(self, *args, **kwargs):  # pylint: disable=arguments-differ
        """Update the timestamp and Sve the Report."""
        self.updated = arrow.utcnow()
        return super().save(*args, **kwargs)
