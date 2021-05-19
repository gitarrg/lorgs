"""Models for Warcraftlog-Reports/Fights/Actors."""

# IMPORT STANDARD LIBRARIES
import datetime

# IMPORT THIRD PARTY LIBRARIES
import mongoengine as me

# IMPORT LOCAL LIBRARIES
from lorgs import db
from lorgs import utils
from lorgs.models.specs import WowSpec
from lorgs.models import warcraftlogs_base
from lorgs.models import encounters
from lorgs.models import warcraftlogs_report


class CompRating(me.Document, warcraftlogs_base.wclclient_mixin):

    # comp_name = me.StringField(required=True)

    comp = me.ReferenceField("CompConfig", required=True) # , reverse_delete_rule=CASCADE)
    boss_slug = me.StringField(required=True)

    updated = me.DateTimeField(default=datetime.datetime.utcnow)

    reports = me.ListField(me.EmbeddedDocumentField(warcraftlogs_report.Report))

    @classmethod
    def get_or_create(cls, **kwargs):
        obj = cls.objects(**kwargs).first()
        obj = obj or cls(**kwargs)
        return obj

    ##########################
    # Attributes
    #
    @property
    def boss(self):
        return encounters.RaidBoss.get(name_slug=self.boss_slug)

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

    ##########################
    # Query
    #

    async def find_top_reports(self, metric="execution", limit=5):
        """Get Top Fights for a given encounter."""
        self.reports = []


        load_more = True
        i = 0

        while load_more:
            query = f"""
            worldData
            {{
                encounter(id: {self.boss.id})
                {{
                    fightRankings(
                        metric: {metric},
                        filter: "{self.comp.report_search}",
                        page: {i+1}
                    )
                }}
            }}
            """
            i += 1

            data = await self.client.query(query)
            data = data.get("worldData", {}).get("encounter", {}).get("fightRankings", {})

            load_more = data.get("hasMorePages", False)

            for ranking_data in data.get("rankings", []):
                report_data = ranking_data.get("report", {})

                ################
                # Report
                report = warcraftlogs_report.Report()
                report.report_id = report_data.get("code", "")
                report.start_time = report_data.get("startTime", 0)
                self.reports.append(report)

                ################
                # Fight
                fight = report.add_fight()
                fight.fight_id = report_data.get("fightID")
                fight.start_time = ranking_data.get("startTime", 0) - report.start_time
                fight.end_time = fight.start_time + ranking_data.get("duration", 0)

                fight.add_boss(self.boss.id)

                if len(self.reports) > limit:
                    return

    async def update(self):

        # reports
        await self.find_top_reports()

        # fights
        fights = utils.flatten(report.fights for report in self.reports)
        await self.load_many(fights, filters=self.comp.get_casts_filters(), chunk_size=5)


class CompConfig(me.Document, warcraftlogs_base.wclclient_mixin):
    """"""

    # uuid = sa.Column(pg.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    name = me.StringField(primary_key=True)

    spec_names = me.ListField(me.StringField())
    report_search = me.StringField()
    casts_filter = me.StringField()

    # boss_reports = me.MapField(me.EmbeddedDocumentField(warcraftlogs_base.Report))
    boss_reports = me.MapField(me.ReferenceField(CompRating))

    """
    spec_id = sa.Column(sa.Integer, sa.ForeignKey("wow_spec.id"))
    spec = sa.orm.relationship("WowSpec", lazy="joined")

    boss_id = sa.Column(sa.Integer, sa.ForeignKey("raid_boss.id"))
    boss = sa.orm.relationship("RaidBoss")

    report_id = sa.Column(sa.String(64))
    fight_id = sa.Column(sa.Integer)
    player_name = sa.Column(sa.Unicode(128))
    name = sa.orm.synonym("player_name")
    amount = sa.Column(sa.Float, default=0)
    total = sa.orm.synonym("amount")

    fight_time_start = sa.Column(sa.BigInteger, default=0)
    fight_time_end = sa.Column(sa.BigInteger, default=0)
    fight_duration = sa.orm.column_property(fight_time_end - fight_time_start)

    cast_data = sa.Column(pg.ARRAY(sa.Integer, dimensions=2), default=[])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    """

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


    async def load_reports(self, boss_slug):

        scr = CompRating.get_or_create(comp=self, boss_slug=boss_slug)
        await scr.update()
        self.boss_reports[boss_slug] = scr
        return scr
