"""Models for Top Rankings for a given Spec."""

# IMPORT STANDARD LIBRARIES
import datetime
import typing
import textwrap

# IMPORT THIRD PARTY LIBRARIES
import arrow
import mongoengine as me

# IMPORT LOCAL LIBRARIES
from lorgs import utils
from lorgs.logger import logger
from lorgs.models import warcraftlogs_base
from lorgs.models.raid_boss import RaidBoss
from lorgs.models.warcraftlogs_actor import BaseActor, Player
from lorgs.models.warcraftlogs_fight import Fight
from lorgs.models.warcraftlogs_report import Report
from lorgs.models.wow_spec import WowSpec


# Map Difficulty Names to Integers used in WCL
DIFFICULTY_IDS: typing.Dict[str, int] = {}
DIFFICULTY_IDS["normal"] = 3
DIFFICULTY_IDS["heroic"] = 4
DIFFICULTY_IDS["mythic"] = 5


class SpecRanking(warcraftlogs_base.Document):

    spec_slug: str = me.StringField(required=True)
    boss_slug: str = me.StringField(required=True)
    difficulty: str = me.StringField(default="")

    updated = me.DateTimeField(default=datetime.datetime.utcnow)

    reports: typing.List[Report] = me.EmbeddedDocumentListField(Report)

    meta = {
        'indexes': [  # type: ignore
            ("boss_slug", "spec_slug", "difficulty"),
            "spec_slug",
            "boss_slug",
            "difficulty",
        ],
        "strict": False # ignore non existing properties
    }

    ##########################
    # Attributes
    #
    @property
    def spec(self) -> WowSpec:
        return WowSpec.get(full_name_slug=self.spec_slug)

    @property
    def boss(self) -> RaidBoss:
        return RaidBoss.get(full_name_slug=self.boss_slug)

    @property
    def fights(self) -> typing.List[Fight]:
        return utils.flatten(report.fights.values() for report in self.reports)

    @property
    def players(self) -> typing.List[Player]:
        return utils.flatten(fight.players.values() for fight in self.fights)

    ##########################
    # Methods
    #
    @staticmethod
    def sort_reports(reports):
        """Sort the reports in place by the highest dps player."""
        def get_total(report: Report):
            top = 0
            for fight in report.fights.values():
                for player in fight.players.values():
                    top = max(top, player.total)
            return top
        return sorted(reports, key=get_total, reverse=True)

    ############################################################################
    # Query: Rankings
    #
    def get_query(self):
        """Return the Query to load the rankings for this Spec & Boss."""
        difficulty_id = DIFFICULTY_IDS.get(self.difficulty, 5)

        return textwrap.dedent(f"""\
        worldData
        {{
            encounter(id: {self.boss.id})
            {{
                characterRankings(
                    className: "{self.spec.wow_class.name_slug_cap}"
                    specName: "{self.spec.name_slug_cap}"
                    metric: {self.spec.role.metric}
                    difficulty: {difficulty_id}
                    includeCombatantInfo: false
                )
            }}
        }}
        """)

    @utils.as_list
    def get_old_reports(self):
        """Return a list of unique keys to identify existing reports."""
        for report in self.reports:
            for fight in report.fights.values():
                for player in fight.players.values():
                    key = (report.report_id, fight.fight_id, player.name)
                    yield key

    def add_new_fight(self, ranking_data):
        report_data = ranking_data.get("report", {})

        if not report_data:
            return

        # skip hidden reports
        if ranking_data.get("hidden"):
            return

        ################
        # Report
        report = Report()
        report.report_id = report_data.get("code", "")
        report.start_time = arrow.get(report_data.get("startTime", 0))
        self.reports.append(report)

        ################
        # Fight
        fight = report.add_fight(
            encounterID=self.boss.id,
            id=report_data.get("fightID"),
        )
        fight.start_time = arrow.get(ranking_data.get("startTime", 0))
        fight.duration = ranking_data.get("duration", 0)

        ################
        # Player
        player = Player()
        player.fight = fight
        player.spec_slug = self.spec_slug
        player.source_id = -1
        player.name = ranking_data.get("name")
        player.total = ranking_data.get("amount", 0)
        player.covenant_id = ranking_data.get("covenantID", 0)
        player.soulbind_id = ranking_data.get("soulbindID", 0)
        fight.players["-1"] = player

    def add_new_fights(self, rankings):
        old_reports = self.get_old_reports()

        for ranking_data in rankings:
            report_data = ranking_data.get("report", {})

            ################
            # check if already in the list
            key = (
                report_data.get("code", ""),
                report_data.get("fightID"),
                ranking_data.get("name")
            )
            if key in old_reports:
                continue

            self.add_new_fight(ranking_data)

    def process_query_result(self, query_result):
        query_result = utils.get_nested_value(
            query_result,
            "worldData", "encounter", "characterRankings", "rankings"
        ) or {}
        self.add_new_fights(query_result)

    async def load_rankings(self):
        """Fetch the current Ranking Data"""
        # Build and run the query
        query = self.get_query()
        query_result = await self.client.query(query)
        self.process_query_result(query_result)

    ############################################################################
    # Query: Fights
    #
    async def load_players(self):
        """Load the Casts for all missing fights."""
        actors_to_load: typing.List[BaseActor] = self.players

        # make sure the first report has the boss added
        if self.fights:
            first_fight = self.fights[0]
            actors_to_load += [first_fight.boss]

        actors_to_load = [actor for actor in actors_to_load if not actor.casts]

        logger.info(f"load {len(actors_to_load)} players")
        if actors_to_load:
            await self.load_many(actors_to_load)

    ############################################################################
    # Query: Both
    #
    async def load(self, limit=50, clear_old=False):
        """Get Top Ranks for a given boss and spec."""
        logger.info(f"{self.boss.name} vs. {self.spec.name} {self.spec.wow_class.name} START | limit={limit} | clear_old={clear_old}")

        if clear_old:
            self.reports = []

        # refresh the ranking data
        await self.load_rankings()
        self.reports = self.sort_reports(self.reports)

        # enforce limit
        limit = limit or -1
        self.reports = self.reports[:limit]

        # load the fights/players/casts
        await self.load_players()

        self.updated = datetime.datetime.utcnow()
        logger.info("done")
