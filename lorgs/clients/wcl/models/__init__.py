"""Models to read in the Data recived from the Warcraflogs API."""

from .character_ranking import (
    CharacterRanking,
    CharacterRankingReportFightData,
    CharacterRankings
)
from .query import Query
from .report_actor import ReportActor
from .report_data import (
    Report,
    ReportData
)
from .report_events import ReportEvent
from .report_fight import ReportFight
from .report_master_data import ReportMasterData

from .report_summary import DeathEvent, ReportSummary
from .world_data import WorldData
