
import uuid

# IMPORT THIRD PARTY LIBRARIES
import sqlalchemy as sa
# from sqlalchemy import Column, ForeignKey
# from sqlalchemy import Integer, String, BigInteger, Unicode, Float
# from sqlalchemy.orm import relationship
# sqlalchemy.ext.declarative.declared_attr

# IMPORT LOCAL LIBRARIES
from lorgs import utils
from lorgs import db


def generate_uuid():
    return str(uuid.uuid4()).replace("-", "")


class BaseCast(db.Base):
    """docstring for Cast"""

    __abstract__ = True

    uuid = sa.Column(sa.CHAR(32), primary_key=True, default=generate_uuid)
    timestamp = sa.Column(sa.Integer)

    # Need to declate the ForeignKey & Relationship as @declared_attr
    # see: https://docs.sqlalchemy.org/en/13/orm/extensions/declarative/mixins.html#mixing-in-relationships

    @sa.ext.declarative.declared_attr
    def spell_id(cls):
        return sa.Column(sa.Integer, sa.ForeignKey("wow_spell.spell_id"))

    @sa.ext.declarative.declared_attr
    def spell(cls):
        return sa.orm.relationship("WowSpell")

    def __repr__(self):
        time_fmt = utils.format_time(self.timestamp)
        return f"Cast({self.spell_id}, at={time_fmt})"

    def as_dict(self):
        return {
            "timestamp": self.timestamp,
            "spell_id": self.spell.spell_id if self.spell else 0,
        }
