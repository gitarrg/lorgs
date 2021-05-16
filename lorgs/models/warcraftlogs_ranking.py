"""Models for Warcraftlog-Reports/Fights/Actors."""

# IMPORT STANDARD LIBRARIES
# import uuid
import datetime

# IMPORT THIRD PARTY LIBRARIES
import mongoengine as me
# import sqlalchemy as sa
# from sqlalchemy.dialects import postgresql as pg

# IMPORT LOCAL LIBRARIES
from lorgs import db
from lorgs import data
from lorgs import utils
from lorgs.logger import logger
from lorgs.models import warcraftlogs_base
from lorgs.models import encounters
from lorgs.models.specs import WowSpec
'''

class RankedCharacter(db.Base):
    """A Character/Player in the top logs."""

    __tablename__ = "ranked_character"

    uuid = sa.Column(pg.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

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

    def __repr__(self):
        amount = utils.format_big_number(self.amount or 0)
        return f"RankedCharacter({self.name}, amount={amount})"

    def as_dict(self):

        return {
            "name": self.name,
            "amount": self.amount,
            "fight": self.fight,
            "casts": [cast.as_dict() for cast in self.casts]
        }


    @property
    def report_url(self):
        return (
            f"https://www.warcraftlogs.com/reports/{self.report_id}"
            f"#fight={self.fight_id}"
            # f"&source={self.source_id}"  # TODO
        )

    @property
    def fight(self):
        return {
            "duration": self.fight_duration,
        }

    @property
    def casts(self):
        cast_data = self.cast_data or []
        return [warcraftlogs_base.Cast(timestamp, spell_id) for timestamp, spell_id in cast_data]



    @property
    def lifetime(self):
        return self.fight_duration

    #################################
    # Query Helpers
    #

    def _get_casts_query(self):
        table_query_args = f"fightIDs: {self.fight_id}, startTime: {self.fight_time_start}, endTime: {self.fight_time_end}"

        spell_ids = ",".join(str(spell.spell_id) for spell in self.spec.spells)
        casts_filter = f"source.name='{self.player_name}' and ability.id in ({spell_ids})"

        return f"""\
            reportData
            {{
                report(code: "{self.report_id}")
                {{
                    casts: events({table_query_args}, dataType: Casts, filterExpression: \"{casts_filter}\")
                        {{data}}
                }}
            }}
            """

    def _process_casts_data(self, casts_data):
        """Process the result of a casts-query to create Cast objects."""
        if not casts_data:
            logger.warning("casts_data is empty")
            return

        self.cast_data = self.cast_data or []

        for cast_data in casts_data:
            # skip "begincast" events
            if cast_data.get("type") != "cast":
                continue

            spell_id = cast_data["abilityGameID"]
            timestamp = cast_data["timestamp"] - self.fight_time_start
            self.cast_data.append([timestamp, spell_id])

'''


class SpecRanking(me.Document, warcraftlogs_base.wclclient_mixin):

    spec_slug = me.StringField(required=True)
    boss_slug = me.StringField(required=True)

    updated = me.DateTimeField(default=datetime.datetime.utcnow)

    reports = me.ListField(me.EmbeddedDocumentField(warcraftlogs_base.Report))

    meta = {
        'indexes': [
            ("boss_slug", "spec_slug"),
            "spec_slug",
            "boss_slug",
        ]
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.spec = WowSpec.get(full_name_slug=self.spec_slug)
        self.boss = encounters.RaidBoss.get(name_slug=self.boss_slug)

    ##########################
    # Attributes
    #

    @property
    def fights(self):
        return utils.flatten(report.fights for report in self.reports)

    @property
    def players(self):
        return utils.flatten(fight.players for fight in self.fights)

    ##########################
    # Methods
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

        # not even needed? because we filter by name
        # logger.debug(f"{boss.name} vs. {spec.name} {spec.wow_class.name} load source ids")
        # await load_char_rankings_source_ids(rankings)

        self.reports = []

        for ranking_data in rankings:
            report_data = ranking_data.get("report", {})

            # skip hidden reports
            if ranking_data.get("hidden"):
                continue

            ################
            # Report
            report = warcraftlogs_base.Report()
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
            player.spec = self.spec
            player.spec_slug = self.spec_slug
            player.source_id = -1 # TODO
            player.name = ranking_data.get("name")
            player.total = ranking_data.get("amount", 0)

        ########################
        # load casts
        #
        logger.info(f"{self.boss.name} vs. {self.spec.name} {self.spec.wow_class.name} load casts")
        for i, chunk in enumerate(utils.chunks(self.fights, 50)): # load in chunks of 50 each
            # logger.info(f"{boss.name} vs. {spec.name} {spec.wow_class.name} load casts | chunk {i}")
            await warcraftlogs_base.Fight.load_many(chunk)

        self.updated = datetime.datetime.utcnow()
