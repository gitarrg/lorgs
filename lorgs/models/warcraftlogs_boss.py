# IMPORT THIRD PARTY LIBRARIES
import typing

# IMPORT LOCAL LIBRARIES
from lorgs.models import warcraftlogs_actor
from lorgs.models.raid_boss import RaidBoss


class Boss(warcraftlogs_actor.BaseActor):
    """A NPC/Boss in a Fight."""

    boss_slug: str
    percent: float = 100.0

    ##########################
    # Attributes
    #
    def __str__(self):
        return f"Boss(slug={self.boss_slug})"

    @property
    def raid_boss(self) -> RaidBoss:
        return RaidBoss.get(full_name_slug=self.boss_slug)

    @classmethod
    def from_raid_boss(cls, raid_boss: RaidBoss) -> "Boss":
        return cls(boss_slug=raid_boss.full_name_slug)

    def as_dict(self) -> dict[str, typing.Any]:
        return {"name": self.raid_boss and self.raid_boss.full_name_slug, "casts": [cast.dict() for cast in self.casts]}

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

    def process_query_result(self, **query_result: typing.Any) -> None:
        query_result = self.raid_boss.preprocess_query_results(**query_result)
        super().process_query_result(**query_result)
