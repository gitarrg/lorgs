"""Models for Top Rankings for a given Spec."""

# IMPORT STANDARD LIBRARIES
import datetime
import typing
import textwrap

# IMPORT THIRD PARTY LIBRARIES
import arrow
import mongoengine as me
import pydantic

# IMPORT LOCAL LIBRARIES
from lorgs import utils
from lorgs.clients import wcl
from lorgs.logger import logger
from lorgs.models import warcraftlogs_base
from lorgs.models.raid_boss import RaidBoss
from lorgs.models.warcraftlogs_fight import Fight
from lorgs.models.warcraftlogs_player import Player
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
    metric: str = me.StringField(default="")
    updated = me.DateTimeField(default=datetime.datetime.utcnow)

    reports: typing.List[Report] = me.EmbeddedDocumentListField(Report)

    meta = {
        'indexes': [  # type: ignore
            ("boss_slug", "spec_slug", "difficulty", "metric"),
            "spec_slug",
            "boss_slug",
            "difficulty",
            "metric",
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
    def fights(self) -> list[Fight]:
        return utils.flatten(report.fights.values() for report in self.reports)

    @property
    def players(self) -> list[Player]:
        return utils.flatten(fight.players.values() for fight in self.fights)

    ##########################
    # Methods
    #
    @staticmethod
    def sort_reports(reports: list[Report]) -> list[Report]:
        """Sort the reports in place by the highest dps player."""
        def get_total(report: Report) -> int:
            top = 0
            for fight in report.fights.values():
                for player in fight.players.values():
                    top = max(top, player.total)
            return top
        return sorted(reports, key=get_total, reverse=True)

    ############################################################################
    # Query: Rankings
    #
    def get_query(self) -> str:
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
                    metric: {self.metric}
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

    def add_new_fight(self, ranking_data: wcl.CharacterRanking) -> None:
        report_data = ranking_data.report

        if not report_data:
            return

        # skip hidden reports
        if ranking_data.hidden:
            return

        ################
        # Report
        report = Report(
            report_id=report_data.code,
            start_time=arrow.get(report_data.startTime),
            # fights={str(fight.fight_id): fight },
        )
        self.reports.append(report)

        ################
        # Fight
        fight = Fight(
            boss_id=self.boss.id,
            fight_id=report_data.fightID,
            start_time = arrow.get(ranking_data.startTime),
            duration = ranking_data.duration,
        )
        fight.report = report
        report.fights[str(fight.fight_id)] = fight

        ################
        # Player
        player = Player(
            source_id=-1,
            name=ranking_data.name,
            total=ranking_data.amount,
            spec_slug=self.spec_slug,
        )
        player.fight = fight
        fight.players["-1"] = player

    def add_new_fights(self, rankings: list[wcl.CharacterRanking]):
        """Add new Fights."""
        old_reports = self.get_old_reports()

        for ranking_data in rankings:
            report_data = ranking_data.report

            ################
            # check if already in the list
            key = (report_data.code, report_data.fightID, ranking_data.name)
            if key in old_reports:
                continue

            self.add_new_fight(ranking_data)

    def process_query_result(self, **query_result: typing.Any):
        """Process the Ranking Results.

        Expected Query:
        >>> {
        >>>     worldData: {
        >>>         encounter: {
        >>>             characterRankings: ....
        >>>         }
        >>>     }
        >>> }
        """ 
        # unwrap data
        query_result = query_result["worldData"]
        world_data = wcl.WorldData(**query_result)

        rankings = world_data.encounter.characterRankings.rankings
        self.add_new_fights(rankings)

    async def load_rankings(self) -> None:
        """Fetch the current Ranking Data"""
        # Build and run the query
        query = self.get_query()
        query_result = await self.client.query(query)
        self.process_query_result(**query_result)

    ############################################################################
    # Query: Fights
    #
    async def load_players(self) -> None:
        """Load the Casts for all missing fights."""
        actors_to_load = self.players

        # make sure the first report has the boss added
        if self.fights:
            first_fight = self.fights[0]
            actors_to_load += [first_fight.boss] # type: ignore

        actors_to_load = [actor for actor in actors_to_load if actor]
        actors_to_load = [actor for actor in actors_to_load if not actor.casts]

        logger.info(f"load {len(actors_to_load)} players")
        if not actors_to_load:
            return

        await self.load_many(actors_to_load, chunk_size=10)

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
