"""Models for Top Rankings for a given Spec."""

# IMPORT STANDARD LIBRARIES
import datetime

# IMPORT THIRD PARTY LIBRARIES
import arrow
import mongoengine as me

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
        return encounters.RaidBoss.get(full_name_slug=self.boss_slug)

    @property
    def fights(self):
        return utils.flatten(report.fights for report in self.reports)

    @property
    def players(self):
        return utils.flatten(fight.players for fight in self.fights)

    @property
    def update_age(self):
        now = arrow.utcnow()
        old = arrow.get(self.updated)
        return now - old

    @property
    def update_age_fmt(self):
        now = arrow.utcnow()
        old = arrow.get(self.updated)
        return old.humanize(now, only_distance=True)

    ##########################
    # Methods
    #
    def sort_reports(self):
        """Sort the reports in place by the highest dps player."""
        def get_dps(report):
            top = 0
            for fight in report.fights:
                for player in fight.players:
                    top = max(top, player.total)
            return top
        self.reports = sorted(self.reports, key=get_dps, reverse=True)

    ##########################
    # Query
    #

    async def load_rankings(self, limit=50):

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
                )
            }}
        }}
        """

        # serverRegion: "EU",
        query_result = await self.client.query(query)
        query_result = query_result.get("worldData", {}).get("encounter", {}).get("characterRankings", {})

        rankings = query_result.get("rankings", [])
        if limit:
            rankings = rankings[:limit]

        return rankings

    async def load(self, limit=50, clear_old=False):
        """Get Top Ranks for a given boss and spec."""
        logger.info(f"{self.boss.name} vs. {self.spec.name} {self.spec.wow_class.name} START | limit={limit} | clear_old={clear_old}")

        rankings = await self.load_rankings(limit=limit)

        if clear_old:
            self.reports = []

        #########################
        #
        #
        old_reports = []
        for report in self.reports:
            for fight in report.fights:
                for player in fight.players:
                    key = (report.report_id, fight.fight_id, player.name)
                    old_reports.append(key)

        new_fights = []
        for ranking_data in rankings:
            report_data = ranking_data.get("report", {})

            # skip hidden reports
            if ranking_data.get("hidden"):
                continue

            ################
            # check if already in the list
            key = (
                report_data.get("code", ""),
                report_data.get("fightID"),
                ranking_data.get("name")
            )
            if key in old_reports:
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

            ################
            # Player
            player = fight.add_player()
            player.spec_slug = self.spec_slug
            player.source_id = -1
            player.name = ranking_data.get("name")
            player.total = ranking_data.get("amount", 0)
            player.covenant_id = ranking_data.get("covenantID", 0)
            player.soulbind_id = ranking_data.get("soulbindID", 0)

            new_fights.append(fight)

        ########################
        # load casts
        #
        if new_fights:
            self.sort_reports()

        # enforce limit
        if limit:
            self.reports = self.reports[:limit]

        # the very first report/fight should always have the boss
        if self.fights:
            first_fight = self.fights[0]
            if not first_fight.boss_id:
                first_fight.add_boss(self.boss.id)
                if first_fight not in new_fights:
                    new_fights.append(first_fight)

        if new_fights:
            logger.info(f"{self.boss.name} vs. {self.spec.name} {self.spec.wow_class.name} load casts | {len(new_fights)} new fights")
            await self.load_many(new_fights)

        self.updated = datetime.datetime.utcnow()
