"""Models for Warcraftlog-Reports/Fights/Actors."""

# IMPORT STANDARD LIBRARIES
import uuid

# IMPORT THIRD PARTY LIBRARIES
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql as pg

# IMPORT LOCAL LIBRARIES
from lorgs import db
from lorgs import utils
# from lorgs.logger import logger
# from lorgs.models import warcraftlogs_base
from lorgs.models.specs import WowSpec


class SpecCombination(db.Base):
    """"""

    __tablename__ = "spec_comp"

    uuid = sa.Column(pg.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    spec_ids = sa.Column(pg.ARRAY(sa.Integer, dimensions=1), default=[])

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
    """

    def __repr__(self):
        spec_names = [spec.name_short for spec in self.specs]
        return f"SpecCombination({spec_names})"

    @property
    def specs(self):
        return [WowSpec.query.get(spec_id) for spec_id in self.spec_ids]

    @specs.setter
    def specs(self, value):
        self.spec_ids = [spec.id for spec in value]


    async def load_top_fights(self):

        query = ""

        self.process_data



