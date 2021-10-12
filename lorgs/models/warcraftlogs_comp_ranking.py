"""Models to store our list of full reports.."""

# IMPORT STANDARD LIBRARIES
import datetime
import typing

# IMPORT THIRD PARTY LIBRARIES
import arrow
import mongoengine as me

# IMPORT LOCAL LIBRARIES
from lorgs import utils
from lorgs.models import encounters
from lorgs.models import specs
from lorgs.models import warcraftlogs_base
from lorgs.models import warcraftlogs_fight
from lorgs.models import warcraftlogs_report


class CompRankingReport(warcraftlogs_base.Document):
    """Wrapper around a Report"""

    report: warcraftlogs_report.Report = me.EmbeddedDocumentField(warcraftlogs_report.Report)
    updated: datetime.datetime = me.DateTimeField(default=datetime.datetime.utcnow)

    meta = {
        "strict": False # ignore non existing properties
    }

    def __repr__(self):
        return f"<{type(self).__name__} {self.key}>"

    def as_dict(self) -> dict:
        d = {}
        d["fight"] = self.fight.as_dict() if self.fight else {}
        return d

    ##########################
    # Attributes
    #
    @property
    def key(self):
        """tuple: a unique key to identify this report."""
        return (self.report.report_id, self.fight.fight_id)

    @property
    def fight(self) -> warcraftlogs_fight.Fight:
        """First Fight found in this report (there should only be one)."""
        for fight in self.report.fights:
            return fight


class CompRanking(warcraftlogs_base.Document):
    """A Group/List of reports for a given Boss."""

    # str: the name of the boss
    boss_slug = me.StringField(required=True)

    # datetime: timetamp of last update
    updated = me.DateTimeField(default=datetime.datetime.utcnow)

    # list(CompRankingReport): reports for this boss
    reports = me.ListField(me.ReferenceField(CompRankingReport))

    ##########################
    # Attributes
    #
    @property
    def valid(self):
        if not self.boss:
            return False
        return True

    @property
    def boss(self) -> encounters.RaidBoss:
        return encounters.RaidBoss.get(full_name_slug=self.boss_slug)

    ##########################
    # Methods
    #
    def get_reports(self, search: dict = None, limit: int = 50) -> typing.List[CompRankingReport]:
        """list: reports for this group."""

        filter_kwargs = {}

        # filter by boss
        filter_kwargs["report__fights__boss__boss_id"] = self.boss.id

        # filter by inputs
        search = search or {}
        # build the search arguments
        for key, value in search.items():
            prefix = f"report.{key}"
            search_kwargs = warcraftlogs_base.query_args_to_mongo(*value, prefix=prefix)
            filter_kwargs.update(search_kwargs)

        # Query
        reports = CompRankingReport.objects  # todo: find a way to use the self.reports list field instead
        reports = reports.filter(**filter_kwargs)
        reports = reports.order_by("+report__fights__deaths", "+report__fights__duration")
        reports = reports[:limit] if limit else reports
        return reports

    def save(self, *args, **kwargs):
        """Custom Cascade safe."""
        for report in self.reports:
            report.save()
        return super().save(*args, **kwargs)

    ############################################################################
    # Query
    #
    @staticmethod
    def _get_healing_cooldowns() -> typing.List[specs.WowSpell]:
        """All Spells that are considered Healing-Cooldowns.

        Right now, this simply returns every spell healers have

        """
        healers = [spec for spec in specs.WowSpec.all if spec.role.code == "heal"]
        spells = utils.flatten(spec.spells for spec in healers)
        spells = [spell for spell in spells if spell.is_healing_cooldown()]
        return spells

    @staticmethod
    def _get_raid_cds() -> typing.List[specs.WowSpell]:
        """All spells of type RAID_CD.

            eg.: Darkness, RallyCry, AMZ
        """
        spells = [spell for spell in specs.WowSpell.all if spell.spell_type== spell.TYPE_RAID]
        return utils.uniqify(spells, key=lambda spell: spell.spell_id)

    @staticmethod
    def _spell_id_filter(spells):
        spell_ids = sorted([spell.spell_id for spell in spells])
        spell_ids = ",".join(str(spell_id) for spell_id in spell_ids)
        return f"type='cast' and ability.id in ({spell_ids})"


    def get_filter(self) -> str:
        """Filter that is applied to the query."""
        healing_cds = self._get_healing_cooldowns()
        healer_filter = "source.role = 'healer'"
        filter_healing_cds = " and ".join([healer_filter, self._spell_id_filter(healing_cds)])

        raid_cds = self._get_raid_cds()
        raid_cds_filter = self._spell_id_filter(raid_cds)

        return f"({filter_healing_cds}) or ({raid_cds_filter})"

    def _get_query(self, metric="execution", page=0) -> str:
        return f"""
            worldData
            {{
                encounter(id: {self.boss.id})
                {{
                    fightRankings(
                        metric: {metric},
                        page: {page}
                    )
                }}
            }}
            """

    def _create_new_report(self, ranking_data):
        ################
        # Wrapper
        comp_report = CompRankingReport()
        comp_report.report = warcraftlogs_report.Report()

        ################
        # Report
        report_data = ranking_data.get("report", {})
        report = comp_report.report
        report.report_id = report_data.get("code", "")
        start_time = report_data.get("startTime", 0)
        report.start_time = arrow.get(start_time)  # wcl returns it in ms

        ################
        # Fight
        fight = report.add_fight()
        fight.fight_id = report_data.get("fightID")
        fight_start = ranking_data.get("startTime", 0)
        fight.start_time = arrow.get(fight_start)
        fight.duration = ranking_data.get("duration", 0)

        fight.deaths = ranking_data.get("deaths", 0)
        fight.damage_taken = ranking_data.get("damageTaken", 0)
        fight.damage_taken = ranking_data.get("damageTaken", 0)
        fight.ilvl = ranking_data.get("bracketData", 0)

        # Boss
        fight.add_boss(self.boss.id)

        return comp_report

    async def load_new_reports(self, metric="execution", limit=5):
        """Get Top Fights for a given encounter."""
        limit = limit or 50  # in case limit defaults to 0 somewhere

        new_reports = []
        load_more = True
        page = 0
        while load_more:  # nobody likes while loops
            page += 1

            # execute the query
            query = self._get_query(metric=metric, page=page)
            data = await self.client.query(query)
            data = data.get("worldData", {}).get("encounter", {}).get("fightRankings", {})

            load_more = data.get("hasMorePages", False)

            # process the result
            for ranking_data in data.get("rankings", []):

                new_report = self._create_new_report(ranking_data)
                new_reports.append(new_report)
                if len(new_reports) >= limit:
                    load_more = False
                    break

        return new_reports

    async def update_reports(self, limit=50, clear_old=False) -> typing.List[CompRankingReport]:
        """Fetch reports for this BossRanking.

        params:
            limit (int): maximum number of reports to load.
            clear_old (bool): if true old reports will be deleted.

        """
        old_reports = self.get_reports()

        # old reports
        if clear_old:
            old_reports.delete()
            old_reports = []
            self.reports = []

        # new reports
        new_reports = await self.load_new_reports(limit=limit)

        # compare old vs new reports
        old_report_keys = [report.key for report  in old_reports]
        new_reports = [report for report in new_reports if report.key not in old_report_keys]

        # load only the fights that need to be loaded
        fights = [report.fight for report in new_reports]
        fights = [fight for fight in fights if not fight.players]
        fights = fights[:limit] # should already be enforced from the "load_new_reports"... but better safe then sorry
        await self.load_many(fights, filters=[self.get_filter()], chunk_size=5)

        self.reports += new_reports