"""Classes/Functions to manage Reports injected through user interaction."""

# IMPORT THIRD PARTY LIBRARIES
import arrow
import mongoengine as me

# IMPORT LOCAL LIBRARIES
from lorgs.lib import mongoengine_arrow
from lorgs.models import warcraftlogs_report


class UserReport(me.Document):  # just me.Document as the WCL-Mixin is not required
    """Shallow Wrapper around a `warcraftlogs_report.Report`.

    Most things should be managed via the Report Instance on: `self.report`

    """
    # datetime: timetamp of last update
    updated: arrow.Arrow = mongoengine_arrow.ArrowDateTimeField(default=arrow.utcnow)

    # the wrapped report object
    report: warcraftlogs_report.Report = me.EmbeddedDocumentField(warcraftlogs_report.Report)

    ################################
    # Properties
    #
    def as_dict(self):
        return {
            "updated": int(self.updated.timestamp()),
            "report": self.report.as_dict(),
        }

    ################################
    # Methods
    #
    async def load(self):
        await self.report.load()
