"""Models to store our list of full reports.."""

# IMPORT STANDARD LIBRARIES
import datetime

# IMPORT THIRD PARTY LIBRARIES
import mongoengine as me

# IMPORT LOCAL LIBRARIES
from lorgs import utils
from lorgs.models.specs import WowSpec
from lorgs.models import warcraftlogs_base
from lorgs.models import encounters
from lorgs.models import warcraftlogs_report



class CompRankingReport(warcraftlogs_base.Document):
    """Wrapper around a Report"""

    # str: the name of the boss
    # boss_slug = me.StringField(required=True)

    report: warcraftlogs_report.Report = me.EmbeddedDocumentField(warcraftlogs_report.Report)
    updated: datetime.datetime = me.DateTimeField(default=datetime.datetime.utcnow)

    # some ranking data
    deaths: int = me.IntField(default=0)


    # report_id = me.StringField(required=True)
    # fight_id = me.IntField(required=True)
    meta = {
        "strict": False # ignore non existing properties
    }
    # meta = {
    #     'indexes': [
    #         ("report_id", "fight_id"),
    #         "report_id",
    #         "fight_id",
    #     ]
    # }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # init some objects
        # self.report = self.report or warcraftlogs_report.Report()
        # self.report.add_fight()

    def __repr__(self):
        return f"<{type(self).__name__} {self.key}>"

    def as_dict(self):

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
    def fight(self):
        for fight in self.report.fights:
            return fight


class CompRanking(warcraftlogs_base.Document):
    """A Group/List of reports for a given Boss."""

    # str: the name of the boss
    boss_slug = me.StringField(required=True)

    # datetime: timetamp of last update
    updated = me.DateTimeField(default=datetime.datetime.utcnow)

    # list of reports
    # reports = me.ListField(me.ReferenceField(CompRankingReport))

    ##########################
    # Attributes
    #
    @property
    def boss(self):
        return encounters.RaidBoss.get(full_name_slug=self.boss_slug)

    """
    @property
    def fights(self):
        return utils.flatten(report.fights for report in self.reports)

    @property
    def players(self):
        players = utils.flatten(fight.players for fight in self.fights)
        players = sorted(players, key=lambda player: (player.spec, player.name))
        return players

    @property
    def spells_used(self):
        spells_used = utils.flatten(player.spells_used for player in self.players)
        spells_used = utils.uniqify(spells_used, key=lambda spell: (spell.group, spell.spell_id))
        spells_used = sorted(spells_used, key=lambda spell: spell.group)
        return spells_used
    """

    ##########################
    # Methods
    #

    def get_reports(self, limit=50):
        """list: reports for this group."""
        reports = CompRankingReport.objects
        reports = reports.filter(
            report__fights__boss__boss_id=self.boss.id
        )
        reports = reports[:limit]
        return reports.all()

    def save(self, *args, **kwargs):
        """Save the Object as well as the included Reports."""
        CompRankingReport.objects.insert(self.reports)
        super().save(*args, **kwargs)


    ##########################
    # Query
    #
    def _get_query(self, metric="execution", page=0):
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
        report.start_time = report_data.get("startTime", 0)

        ################
        # Fight
        fight = report.add_fight()
        fight.fight_id = report_data.get("fightID")
        fight.start_time = ranking_data.get("startTime", 0) - report.start_time
        fight.end_time = fight.start_time + ranking_data.get("duration", 0)

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

    async def update_reports(self, limit=50, clear_old=False):

        # old reports
        if clear_old:
            self.reports = [] # FIXME

        # new reports
        new_reports = await self.load_new_reports(limit=limit)

        # compare old vs new reports
        old_reports = self.get_reports()    
        old_report_keys = [report.key for report  in old_reports]
        new_reports = [report for report in new_reports if report.key not in old_report_keys]

        print("actually new_reports", new_reports)

        # load only the fights that need to be loaded
        fights = [report.fight for report in new_reports]
        fights = [fight for fight in fights if not fight.players]
        fights = fights[:limit] # should already be enforced from the "load_new_reports"... but better safe then sorry
        # fights = [fights[0]]
        # print("fights to load", fights)
        await self.load_many(fights, chunk_size=5)

'''


class CompType(me.Document, warcraftlogs_base.wclclient_mixin):
    """"""

    name = me.StringField(primary_key=True)

    report_search = me.StringField()
    casts_filter = me.StringField()
    boss_reports = me.MapField(me.ReferenceField(CompRating))

    def __repr__(self):
        spec_names = [spec.name_short for spec in self.specs]
        return f"SpecCombination({spec_names})"

    def as_dict(self):
        return self.to_json()

    @classmethod
    def get_or_create(cls, **kwargs):
        obj = cls.objects(**kwargs).first()
        obj = obj or cls(**kwargs)
        return obj

    ##########################
    # Attributes
    #

    @property
    def specs(self):
        return [WowSpec.get(full_name_slug=spec_name) for spec_name in self.spec_names]

    @specs.setter
    def specs(self, value):
        self.spec_names = [spec.full_name_slug for spec in value]

    ##########################
    # Query
    #
    def get_casts_filters(self):
        spells = utils.flatten(spec.spells for spec in self.specs)

        spell_ids = [spell.spell_id for spell in spells]
        spell_ids = sorted(list(set(spell_ids)))
        spell_ids = ",".join(str(spell_id) for spell_id in spell_ids)

        return [self.casts_filter, "type='cast'", f"ability.id in ({spell_ids})"]


    async def load_reports(self, boss_slug, limit=50, clear_old=False):

        scr = CompRating.get_or_create(comp=self, boss_slug=boss_slug)
        await scr.update(limit=limit, clear_old=clear_old)
        self.boss_reports[boss_slug] = scr
        return scr

'''