

# IMPORT STANRD LIBRARIES
import datetime

# IMPORT THIRD PARTY LIBRARIES
import mongoengine as me

# IMPORT LOCAL LIBRARIES
from lorgs import data
from lorgs import utils
from lorgs.models import warcraftlogs_base
from lorgs.models.warcraftlogs_actor import Boss
from lorgs.models.warcraftlogs_fight import Fight


class Report(warcraftlogs_base.EmbeddedDocument):

    report_id = me.StringField(primary_key=True)
    start_time = me.IntField(default=0)

    title = me.StringField()

    fights = me.ListField(me.EmbeddedDocumentField(Fight))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for fight in self.fights:
            fight.report = self

    def __str__(self):
        return f"<BaseReport({self.report_id}, num_fights={len(self.fights)})>"

    ##########################
    # Attributes
    #
    @property
    def players(self):
        return utils.flatten(fight.players for fight in self.fights)

    @property
    def report_url(self):
        return f"https://www.warcraftlogs.com/reports/{self.report_id}/"

    ##########################
    # Methods
    #

    def add_fight(self, **kwargs):
        fight = Fight(**kwargs)
        fight.report = self
        self.fights.append(fight)
        return fight

    ##########################
    # Query
    #

    async def load_report_info(self, fight_ids=None):
        """Fetch all fights in this report.

        Args:
            fight_ids(list[int], optional): list of fights to load.
                loads all fights, if not specified.

        """
        query = f"""
        reportData
        {{
            report(code: "{self.report_id}")
            {{
                title
                zone {{name id}}
                startTime

                # masterData
                # {{
                #     actors(type: "Player")
                #     {{
                #         name
                #         id
                #     }}
                # }}

                fights(fightIDs: {fight_ids or []})
                {{
                    id
                    encounterID
                    startTime
                    endTime
                    fightPercentage
                    # kill
                }}
            }}
        }}
        """

        query_result = await self.client.query(query)
        report_data = query_result.get("reportData", {}).get("report", {})

        # Update the Report itself
        self.title = report_data.get("title", "")
        self.start_time = report_data.get("startTime", 0)

        # Update the Fights in this report
        for fight_data in report_data.get("fights", []):

            # skip trash fights
            boss_id = fight_data.get("encounterID")
            if not boss_id:
                continue

            # Get the fight
            fight = self.add_fight()
            fight.fight_id = fight_data.get("id")
            fight.start_time = fight_data.get("startTime", 0)
            fight.end_time = fight_data.get("endTime", 0)
            fight.boss = Boss(boss_id=boss_id)
            fight.boss.fight = fight
            fight.boss.percent = fight_data.get("fightPercentage")

    async def load(self, fight_ids=None):

        await self.load_report_info(fight_ids)
        await self.load_many(self.fights)


class UserReport(me.Document):
    """docstring for UserReport"""

    report_id = me.StringField(primary_key=True)
    report = me.EmbeddedDocumentField(Report)

    created = me.DateTimeField(default=datetime.datetime.utcnow)
    meta = {
        'indexes': [
            {'fields': ['created'], 'expireAfterSeconds': 7 * 24 * 60 * 60} # expires after 1 week
        ]
    }

    async def load(self, **kwargs):
        self.report = Report(report_id=self.report_id)
        await self.report.load(**kwargs)

    @classmethod
    def get_or_create(cls, **kwargs):
        obj = cls.objects(**kwargs).first()
        obj = obj or cls(**kwargs)
        return obj
