# IMPORT THIRD PARTY LIBRARIES
import typing

# IMPORT LOCAL LIBRARIES
from lorgs.models import warcraftlogs_actor
from lorgs.models.raid_boss import RaidBoss

if typing.TYPE_CHECKING:
    from lorgs.models.wow_actor import WowActor


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
        raid_boss = RaidBoss.get(full_name_slug=self.boss_slug)
        if not raid_boss:
            raise ValueError(f"Invalid boss_slug: {self.boss_slug}")
        return raid_boss

    def get_actor_type(self) -> "WowActor":
        return self.raid_boss

    @classmethod
    def from_raid_boss(cls, raid_boss: RaidBoss) -> "Boss":
        return cls(boss_slug=raid_boss.full_name_slug)

    def as_dict(self) -> dict[str, typing.Any]:
        return {"name": self.raid_boss and self.raid_boss.full_name_slug, "casts": [cast.dict() for cast in self.casts]}
