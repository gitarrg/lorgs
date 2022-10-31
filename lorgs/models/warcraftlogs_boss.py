# IMPORT THIRD PARTY LIBRARIES
import typing
import mongoengine as me

# IMPORT LOCAL LIBRARIES
from lorgs.models import warcraftlogs_actor
from lorgs.models.raid_boss import RaidBoss

if typing.TYPE_CHECKING:
    from lorgs.clients import wcl


class Boss(warcraftlogs_actor.BaseActor):
    """A NPC/Boss in a Fight."""

    boss_id = me.IntField(required=True)
    percent = me.FloatField(default=100)

    ##########################
    # Attributes
    #
    def __str__(self):
        return f"Boss(id={self.boss_id})"

    @property
    def raid_boss(self) -> RaidBoss:
        return RaidBoss.get(id=self.boss_id)

    def as_dict(self) -> dict[str, typing.Any]:
        return {
            "name": self.raid_boss and self.raid_boss.full_name_slug,
            "casts": [cast.as_dict() for cast in self.casts]
        }

    #################################
    # Query
    #
    def get_sub_query(self):
        """Get the Query for fetch all relevant data for this Boss."""
        if not self.raid_boss:
            return ""

        cast_query = self.get_cast_query(self.raid_boss.spells)
        buffs_query = self.get_buff_query(self.raid_boss.buffs)
        events_query = self.raid_boss.get_events_query()

        return self.combine_queries(cast_query, buffs_query, events_query)

    def process_query_result(self, query_result: "wcl.Query"):
        query_result = self.raid_boss.preprocess_query_results(query_result)
        return super().process_query_result(query_result)
