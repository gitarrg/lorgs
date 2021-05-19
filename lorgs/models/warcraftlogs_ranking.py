"""Models for Warcraftlog-Reports/Fights/Actors."""

# IMPORT STANDARD LIBRARIES
# import uuid
import datetime

# IMPORT THIRD PARTY LIBRARIES
import mongoengine as me
# import sqlalchemy as sa
# from sqlalchemy.dialects import postgresql as pg

# IMPORT LOCAL LIBRARIES
from lorgs import utils
from lorgs.logger import logger
from lorgs.models import encounters
from lorgs.models import warcraftlogs_base
from lorgs.models import warcraftlogs_report
from lorgs.models.specs import WowSpec


class SpecRanking(warcraftlogs_base.Document):

    spec_slug = me.StringField(required=True)
    boss_slug = me.StringField(required=True)

    updated = me.DateTimeField(default=datetime.datetime.utcnow)

    reports = me.ListField(me.EmbeddedDocumentField(warcraftlogs_report.Report))

    meta = {
        'indexes': [
            ("boss_slug", "spec_slug"),
            "spec_slug",
            "boss_slug",
        ]
    }

    ##########################
    # Attributes
    #
    @property
    def spec(self):
        return WowSpec.get(full_name_slug=self.spec_slug)

    @property
    def boss(self):
        return encounters.RaidBoss.get(name_slug=self.boss_slug)

    @property
    def fights(self):
        return utils.flatten(report.fights for report in self.reports)

    @property
    def players(self):
        return utils.flatten(fight.players for fight in self.fights)

    ##########################
    # Query
    #
    async def load(self, limit=50):
        """Get Top Ranks for a given boss and spec."""
        logger.info(f"{self.boss.name} vs. {self.spec.name} {self.spec.wow_class.name} START | limit={limit}")

        # Build and run the query
        query = f"""\
        worldData
        {{
            encounter(id: {self.boss.id})
            {{
                characterRankings(
                    className: "{self.spec.wow_class.name_slug_cap}",
                    specName: "{self.spec.name_slug_cap}",
                    metric: {self.spec.role.metric},
                    includeCombatantInfo: false,
                    serverRegion: "EU",
                )
            }}
        }}
        """
        query_result = await self.client.query(query)
        query_result = query_result.get("worldData", {}).get("encounter", {}).get("characterRankings", {})

        rankings = query_result.get("rankings", [])
        if limit:
            rankings = rankings[:limit]


        self.reports = []

        for ranking_data in rankings:
            report_data = ranking_data.get("report", {})

            # skip hidden reports
            if ranking_data.get("hidden"):
                continue

            ################
            # Report
            report = report = warcraftlogs_report.Report()
            report.report_id = report_data.get("code", "")
            report.start_time = report_data.get("startTime", 0)
            self.reports.append(report)

            ################
            # Fight
            fight = report.add_fight()
            fight.fight_id = report_data.get("fightID")
            fight.start_time = ranking_data.get("startTime", 0) - report.start_time
            fight.end_time = fight.start_time + ranking_data.get("duration", 0)

            if len(self.reports) == 1: # this is the first report
                fight.add_boss(self.boss.id)

            ################
            # Player
            player = fight.add_player()
            player.spec_slug = self.spec_slug
            player.source_id = -1
            player.name = ranking_data.get("name")
            player.total = ranking_data.get("amount", 0)

        ########################
        # load casts
        #
        logger.info(f"{self.boss.name} vs. {self.spec.name} {self.spec.wow_class.name} load casts")
        # for fight in self.fights:
        #     print(fight.get_query())

        await self.load_many(self.fights)
        self.updated = datetime.datetime.utcnow()
