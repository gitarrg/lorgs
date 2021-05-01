"""Models for Warcraftlog-Reports/Fights/Actors."""

# pylint: disable=too-few-public-methods

# IMPORT STANRD LIBRARIES
# import datetime
import arrow

# IMPORT LOCAL LIBRARIES
from lorgs import utils
from lorgs.logger import logger

from lorgs.models import base
from lorgs.cache import Cache
from lorgs.models.specs import WowClass
from lorgs.models.specs import WowSpec
from lorgs.models.specs import WowSpell
from lorgs.models.encounters import RaidZone
from lorgs.models.encounters import RaidBoss


class SpecRanking(base.Model):

    def __init__(self, spec, boss):
        self.last_update = 0
        self.spec = spec
        self.boss = boss
        self.cache_key = f"spec_ranking/{self.spec.full_name_slug}/{self.boss.name_slug}"

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


class Report(base.Model):
    """docstring for Fight"""

    def __init__(self, report_id: str):
        self.report_id = report_id
        self.title = ""
        self.start_time = 0
        self.zone = None
        self.fights = []

    def __repr__(self):
        return f"<Report({self.report_id})>"

    @classmethod
    def from_dict(cls, state):

        report_id = state.get("report_id")
        self = cls(report_id)
        self.title = state.get("title")
        self.start_time = state.get("start_time")
        self.zone = RaidZone.get(**state.get("zone", {}))

        self.fights = []
        for fight_data in state.get("fights", []):
            self.add_fight(**fight_data)

        return self

    def as_dict(self):
        return {
            "report_id": self.report_id,
            "title": self.title,
            "start_time": self.start_time,
            "zone": self.zone.as_dict() if self.zone else {},
            "fights": [fight.as_dict() for fight in self.fights]
        }

    def add_fight(self, **kwargs):
        fight = Fight(**kwargs)
        fight.report = self
        self.fights.append(fight)
        return fight

    @property
    def report_url(self):
        return f"https://www.warcraftlogs.com/reports/{self.report_id}"

    @property
    def players(self):
        players = utils.flatten(fight.players for fight in self.fights)
        return utils.uniqify(players, key=lambda player: player.source_id)

    @property
    def used_spells(self):
        spells = utils.flatten(fight.used_spells for fight in self.fights)
        return utils.uniqify(spells, key=lambda spell: spell.spell_id)


class Fight(base.Model):
    """Basically a pull."""

    def __init__(self, fight_id=0, start_time=0, end_time=0, percent=0, **kwargs):
        super().__init__()

        self.fight_id = fight_id
        self.start_time = start_time
        self.end_time = end_time
        self.percent = percent

        self.report = None

        boss_id = kwargs.get("boss_id") or kwargs.get("boss", {}).get("id")
        self.boss = RaidBoss.get(id=boss_id) if boss_id else None

        self.players = []
        for player_data in kwargs.get("players", []):
            self.add_player(**player_data)

    def __repr__(self):
        return f"Fight({self.report.report_id}, id={self.fight_id}, players={len(self.players)})"

    @classmethod
    def from_dict(cls, data):
        return cls(**data)
        # fight.players = [Fight.from_dict(fight_data) for fight_data in data.get("fights", [])]

    def as_dict(self):
        return {
            "fight_id": self.fight_id,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "percent": self.percent,
            "boss": self.boss.as_dict() if self.boss else {},
            "players": [player.as_dict() for player in self.players],
        }

    def add_player(self, **kwargs):
        player = Player(**kwargs)
        player.fight = self
        self.players.append(player)
        return player

    ##########################
    # Attributes

    @property
    def duration(self):
        return self.end_time - self.start_time

    @property
    def report_url(self):
        return f"{self.report.report_url}#fight={self.fight_id}"

    @property
    def used_spells(self):
        spells = utils.flatten(player.used_spells for player in self.players)
        return utils.uniqify(spells, key=lambda spell: spell.spell_id)

    @property
    def percent_color(self):
        if self.percent < 3:
            return "astounding"
        if self.percent < 10:
            return "legendary"
        if self.percent < 25:
            return "epic"
        if self.percent < 50:
            return "rare"
        if self.percent < 75:
            return "uncommon"
        return "common"


class Player(base.Model):
    """a player in a given fight.

    TODO:
        rename to actor?

    """
    def __init__(self, source_id=0, name="", total=0, **kwargs):
        super().__init__()
        self.source_id = source_id
        self.name = name
        self.total = total

        self.fight = None

        spec_name = kwargs.get("spec")
        self.spec = WowSpec.get(full_name_slug=spec_name) if spec_name else None

        self.casts = []
        for cast_data in kwargs.get("casts", []):
            self.add_cast(**cast_data)

    def __repr__(self):
        return f"Player({self.name} spec={self.spec.name} id={self.source_id} casts={len(self.casts)})"

    def __setstate__(self, state):
        self.source_id = state["source_id"]
        self.name = state["name"]
        self.total = state["total"]

        spec_name = state.get("spec")
        self.spec = WowSpec.get(full_name_slug=spec_name) if spec_name else None

        self.casts = []
        for cast_data in state.get("casts", []):
            self.add_cast(**cast_data)

    def as_dict(self):
        return {
            "source_id": self.source_id,
            "name": self.name,
            "total": self.total,
            "spec": self.spec.full_name_slug if self.spec else "",
            "casts": [cast.as_dict() for cast in self.casts]
        }

    @property
    def report_url(self):
        return f"{self.fight.report_url}&source={self.source_id}"

    @property
    def used_spells(self):
        spells = [cast.spell for cast in self.casts]
        return utils.uniqify(spells, key=lambda spell: spell.spell_id)

    def add_cast(self, **kwargs):
        cast = Cast(**kwargs)
        cast.player = self
        self.casts.append(cast)
        return cast


class Cast(base.Model):
    """docstring for Cast"""

    def __init__(self, timestamp=0, spell_id=None, **kwargs):
        super().__init__()
        self.timestamp = timestamp
        self.player = None
        self.spell_id = spell_id

    def __repr__(self):
        time_fmt = utils.format_time(self.time)
        return f"Cast({self.spell.spell_id}, at={time_fmt})"

    def as_dict(self):
        return {
            "timestamp": self.timestamp,
            "spell_id": self.spell.spell_id if self.spell else 0,
        }

    @property
    def spell(self):
        spec = self.player.spec
        return WowSpell.get(spec=spec, spell_id=self.spell_id)

    @property
    def time(self):
        return self.timestamp - self.player.fight.start_time
