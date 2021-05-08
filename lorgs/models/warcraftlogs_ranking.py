
"""Models for Warcraftlog-Reports/Fights/Actors."""

# pylint: disable=too-few-public-methods
# pylint: disable=maybe-no-member

# IMPORT STANRD LIBRARIES
# import datetime
# import arrow
# import textwrap


# IMPORT THIRD PARTY LIBRARIES
import sqlalchemy as sa

# IMPORT LOCAL LIBRARIES
from lorgs import utils
from lorgs.logger import logger

# from lorgs.models import base
# from lorgs.cache import Cache
# from lorgs.models.specs import WowClass
# from lorgs.models.specs import WowSpec
# from lorgs.models.specs import WowSpell
# from lorgs.models.encounters import RaidZone
# from lorgs.models.encounters import RaidBoss
# from lorgs.client import WarcraftlogsClient

# from lorgs.models import warcraftlogs
from lorgs.models import warcraftlogs_base
from lorgs import db
# from lorgs import utils



class RankedCharacterCast(warcraftlogs_base.BaseCast):

    __tablename__ = "ranked_character_cast"

    player_uuid = sa.Column(sa.CHAR(32), sa.ForeignKey("ranked_character.uuid", ondelete="cascade"))
    player = sa.orm.relationship("RankedCharacter", back_populates="casts")


class RankedCharacter(db.Base):
    """docstring for RankedCharacter"""

    __tablename__ = "ranked_character"

    uuid = sa.Column(sa.CHAR(32), primary_key=True)

    spec_id = sa.Column(sa.Integer, sa.ForeignKey("wow_spec.id"))
    spec = sa.orm.relationship("WowSpec")

    boss_id = sa.Column(sa.Integer, sa.ForeignKey("raid_boss.id"))
    boss = sa.orm.relationship("RaidBoss")

    report_id = sa.Column(sa.String(64))
    fight_id = sa.Column(sa.Integer)
    player_name = sa.Column(sa.Unicode(128))
    name = sa.orm.synonym("player_name")

    fight_time_start = sa.Column(sa.BigInteger)
    fight_time_end = sa.Column(sa.BigInteger)
    amount = sa.Column(sa.Float, default=0)
    total = sa.orm.synonym("amount")

    casts = sa.orm.relationship(
        "RankedCharacterCast",
        back_populates="player",
        cascade="all,save-update,delete"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # make sure to generate a uuid on object created,
        # so we can use it pre-commit to setup relationships
        self.uuid = warcraftlogs_base.generate_uuid()

    def __repr__(self):
        amount = utils.format_big_number(self.amount)
        return f"RankedCharacter({self.player_name}, amount={amount})"

    @property
    def report_url(self):
        return (
            f"https://www.warcraftlogs.com/reports/{self.report_id}"
            f"#fight={self.fight_id}"
            # f"&source={self.source_id}"  # TODO
        )

    @property
    def fight_duration(self):
        return self.fight_time_end - self.fight_time_start

    @property
    def fight(self):
        return {
            "duration": self.fight_duration,
        }

    @property
    def spells_used(self):
        """Only the spells this player has used in this fight."""
        used_spell_ids = set(cast.spell_id for cast in self.casts)
        return [spell for spell in self.spec.spells if spell.spell_id in used_spell_ids]

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

        for cast_data in casts_data:
            # skip "begincast" events
            if cast_data.get("type") != "cast":
                continue

            cast = RankedCharacterCast()
            # cast.player = self
            cast.player_uuid = self.uuid
            cast.timestamp = cast_data["timestamp"]
            cast.spell_id = cast_data["abilityGameID"]

            # offset the timestamp (saves us some work later)
            cast.timestamp -= self.fight_time_start
            self.casts.append(cast)


class SpecRanking(db.Base):

    __tablename__ = "spec_ranking"

    # TODO:
    # >>> This is not used anywhere?

    spec_id = sa.Column(sa.Integer, sa.ForeignKey("wow_spec.id"), primary_key=True)
    boss_id = sa.Column(sa.Integer, sa.ForeignKey("raid_boss.id"), primary_key=True)

    boss = sa.orm.relationship("RaidBoss")

    # last_update = sa.Column(db.Integer)
    characters = sa.orm.relationship("RaidBoss")

    def __init__(self, spec, boss):
        self.last_update = 0
        self.spec = spec
        self.boss = boss
        # self.cache_key = f"spec_ranking/{self.spec.full_name_slug}/{self.boss.name_slug}"
        self.reports = []

    def __repr__(self):
        return f"<SpecRanking({self.spec.full_name} vs {self.boss.name})>"

    def as_dict(self):
        return {
            "spec": self.spec.full_name_slug,
            "boss": self.boss.as_dict(),

            "last_update": self.last_update,
            "reports": [report.as_dict() for report in self.reports]
        }

    """
    async def update(self, limit=50, force=True):
        from lorgs.models import loader

        players = await loader.load_char_rankings(boss=self.boss, spec=self.spec, limit=limit)

        self.reports = [player.fight.report for player in players]
        self.last_update = arrow.utcnow().timestamp()
        self.save()

    def save(self):
        Cache.set(self.cache_key, self.as_dict())

    def load(self):

        data = Cache.get(self.cache_key) or {}

        self.last_update = data.get("last_update") or self.last_update
        for report_data in data.get("reports", []):
            report = Report.from_dict(report_data)
            self.reports.append(report)
    """