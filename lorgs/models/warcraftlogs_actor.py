
# IMPORT STANRD LIBRARIES
import abc
import textwrap
import typing

# IMPORT THIRD PARTY LIBRARIES
import mongoengine as me

# IMPORT LOCAL LIBRARIES
from lorgs import utils
from lorgs.logger import logger
from lorgs.models import warcraftlogs_base
from lorgs.models.raid_boss import RaidBoss
from lorgs.models.wow_spec import WowSpec
from lorgs.models.wow_spell import WowSpell
from lorgs.models.wow_covenant import WowCovenant


class Cast(me.EmbeddedDocument):
    """docstring for Cast"""

    timestamp = me.IntField()
    spell_id = me.IntField()
    duration = me.IntField()

    def __str__(self):
        time_fmt = utils.format_time(self.timestamp)
        return f"Cast({self.spell_id}, at={time_fmt})"

    def as_dict(self):
        dict = {
            "ts": self.timestamp,
            "id": self.spell_id,
        }
        if self.duration:
            dict["d"] = self.duration
        return dict

    ##########################
    # Attributes
    #
    @property
    def spell(self):
        return WowSpell.get(spell_id=self.spell_id)

    @property
    def end_time(self):
        return self.timestamp + (self.duration * 1000)

    @end_time.setter
    def end_time(self, value):
        self.duration = (value - self.timestamp) / 1000


class BaseActor(warcraftlogs_base.EmbeddedDocument):
    """Base Class for any Actor in a Fight.

    these are usually either Players or NPC/Bosses

    """

    # list of cast
    casts = me.ListField(me.EmbeddedDocumentField(Cast))
    source_id = -1

    meta = {
        'abstract': True,
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # backref to the parent fight object
        self.fight = None

    ##########################
    # Attributes
    #
    @property
    def _has_source_id(self):
        return self.source_id >= 0

    #################################
    # Query
    #
    def get_cast_query(self, spells=typing.List[WowSpell]):
        if not spells:
            return ""

        spell_ids = WowSpell.spell_ids_str(spells)
        cast_filter = f"type='cast' and ability.id in ({spell_ids})"
        return cast_filter

    def get_buff_query(self, spells=typing.List[WowSpell]):
        if not spells:
            return ""
        # we check for "removebuff" as this allows us to also catch buffs
        # that get used prepull (eg.: lust)
        spell_ids = WowSpell.spell_ids_str(spells)
        buffs_query = f"type in ('applybuff', 'removebuff') and ability.id in ({spell_ids})"
        return buffs_query

    @abc.abstractmethod
    def get_sub_query(self, filters=None):
        return ""

    def get_query(self, filters=None):
        return textwrap.dedent(f"""\
            reportData
            {{
                report(code: "{self.fight.report.report_id}")
                {{
                    {self.get_sub_query(filters)}
                }}
            }}
        """)

    def process_query_result(self, query_result):
        """Process the result of a casts-query to create Cast objects."""

        # save unwrap the data
        query_result = query_result.get("reportData") or query_result
        query_result = query_result.get("report") or query_result
        query_result = query_result.get("events") or query_result

        casts_data = query_result.get("data") or []
        if not casts_data:
            logger.warning("casts_data is empty")
            return

        active_buffs: typing.Dict[int, Cast] = {}

        for cast_data in casts_data:

            # TODO: fetch source_id's?
            if self._has_source_id and cast_data.get("sourceID") != self.source_id:
                continue

            # Add the Cast Object
            cast = Cast()
            cast.spell_id = cast_data["abilityGameID"]
            cast.timestamp = cast_data["timestamp"] - self.fight.start_time_rel

            # we check if the buff was applied before..
            if cast_data["type"] == "removebuff":
                start_cast = active_buffs.get(cast.spell_id)

                # special case for buffs that are applied pre pull
                # meaning.. the buff was already present at the start of the fight,
                if not start_cast:
                    spell = WowSpell.get(spell_id=cast.spell_id) # get the duration from the spell defintion
                    cast.timestamp -= (spell.duration * 1000) # and calculate back the start time

                # if we have a start cast, we can calculate the correct duration
                else:
                    start_cast.duration = (cast.timestamp - start_cast.timestamp) / 1000
                    continue # stop the loop here

            self.casts.append(cast)

            # track applied buffs
            active_buffs[cast.spell_id] = cast

        # Filter out same event at the same time (eg.: raid wide debuff apply)
        self.casts = utils.uniqify(self.casts, key=lambda cast: (cast.spell_id, cast.timestamp))
        self.casts = list(self.casts) # `utils.uniqify` returns dict values, which mongoengine doesn't like

        # make sure casts are sorted correctly
        # avoids weird UI overlaps, and just feels cleaner
        self.casts = sorted(self.casts, key=lambda cast: cast.timestamp)


class Player(BaseActor):
    """A PlayerCharater in a Fight (or report)."""

    source_id = me.IntField(primary_key=True)
    name = me.StringField(max_length=12) # names can be max 12 chars
    total = me.FloatField(default=0)

    class_slug = me.StringField()
    spec_slug = me.StringField(required=True)

    covenant_id = me.IntField(default=0)
    soulbind_id = me.IntField(default=0)

    deaths = me.ListField(me.DictField())

    def __str__(self):
        return f"Player(id={self.source_id} name={self.name} spec={self.spec})" # casts={len(self.casts)})"

    def summary(self):
        return {
            "name": self.name,
            "source_id": self.source_id,
            "class": self.spec.wow_class.name_slug,

            "spec": self.spec_slug,
            "role": self.spec.role.code,
        }

    def as_dict(self):
        return {
            **self.summary(),
            "total": int(self.total),
            "covenant": self.covenant.name_slug,
            "casts": [cast.as_dict() for cast in self.casts],
        }

    ##########################
    # Attributes
    #
    @property
    def spec(self) -> WowSpec:
        return WowSpec.get(full_name_slug=self.spec_slug)

    @property
    def covenant(self) -> WowCovenant:
        return WowCovenant.get(id=self.covenant_id or 0)

    @property
    def report_url(self):
        if self._has_source_id:
            return f"{self.fight.report_url}&source={self.source_id}"
        return f"{self.fight.report_url}"

    #################################
    # Query
    #
    def get_cast_query(self, spells=typing.List[WowSpell]):
        cast_query = super().get_cast_query(spells=spells)
        if self.name:
            cast_query = f"source.name='{self.name}' and {cast_query}"
        return cast_query

    def get_buff_query(self, spells=typing.List[WowSpell]):
        buffs_query = super().get_buff_query(spells=spells)
        if self.name:
            buffs_query = f"target.name='{self.name}' and {buffs_query}"
        return buffs_query

    def get_sub_query(self, filters=None) -> str:
        """Get the Query for fetch all relevant data for this player."""
        filters = filters or []

        cast_query = self.get_cast_query(self.spec.all_spells)
        filters.append(cast_query)

        buffs_query = self.get_buff_query(self.spec.all_buffs)
        filters.append(buffs_query)

        # combine all filters
        filters = [f for f in filters if f]   # fitler the filters
        filters = [f"({f})" for f in filters] # wrap each filter into bracers
        filters = " or ".join(filters)
        return filters

    def process_death_events(self, death_events):
        ability_overwrites = {}
        ability_overwrites[1] = {"name": "Melee", "guid": 260421, "abilityIcon": "ability_meleedamage.jpg"}
        ability_overwrites[3] = {"name": "Fall Damage"}

        for death_event in death_events:

            if death_event.get("id") != self.source_id:
                continue

            death_data = {}
            death_data["deathTime"] = death_event.get("deathTime")
            death_data["ability"] = death_event.get("ability", {})

            # Ability Overwrites
            ability_id = death_data["ability"].get("guid")
            if ability_id in ability_overwrites:
                death_data["ability"] = ability_overwrites[ability_id]

            self.deaths.append(death_data)


class Boss(BaseActor):
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

    def as_dict(self):
        return {
            "name": self.raid_boss.full_name_slug,
            "casts": [cast.as_dict() for cast in self.casts]
        }
