
# IMPORT STANRD LIBRARIES
import abc
import textwrap
import typing
import math

# IMPORT THIRD PARTY LIBRARIES
import mongoengine as me

# IMPORT LOCAL LIBRARIES
from lorgs import utils
from lorgs.logger import logger
from lorgs.models import warcraftlogs_base
from lorgs.models.warcraftlogs_cast import Cast
from lorgs.models.wow_covenant import WowCovenant
from lorgs.models.wow_spec import WowSpec
from lorgs.models.wow_spell import WowSpell



class BaseActor(warcraftlogs_base.EmbeddedDocument):
    """Base Class for any Actor in a Fight.

    these are usually either Players or NPC/Bosses

    """

    # list of cast
    casts: typing.List[Cast] = me.ListField(me.EmbeddedDocumentField(Cast))
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

    @property
    def has_own_casts(self):
        """Return true if a player has own casts (eg.: exclude raid wide buffs like bloodlust)."""
        for cast in self.casts:
            spell = WowSpell.get(spell_id=cast.spell_id)

            if spell.spell_type != WowSpell.TYPE_BUFFS:
                return True
        return False

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

        # TODO: split buffs/debuffs for performance?
        event_types = ["applybuff", "removebuff", "applydebuff", "removedebuff"]
        event_types = [f"'{event}'" for event in event_types]
        event_types = ",".join(event_types)

        buffs_query = f"type in ({event_types}) and ability.id in ({spell_ids})"
        return buffs_query

    @abc.abstractmethod
    def get_sub_query(self):
        return ""

    def get_query(self):
        return textwrap.dedent(f"""\
            reportData
            {{
                report(code: "{self.fight.report.report_id}")
                {{
                    events({self.fight.table_query_args}, filterExpression: "{self.get_sub_query()}")
                        {{data}}
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

        fight_start = self.fight.start_time_rel if self.fight else 0

        for cast_data in casts_data:
            cast_type: str = cast_data.get("type") or "unknown"

            cast_actor_id = cast_data.get("sourceID")
            if cast_type in ("applybuff", "removebuff"):
                cast_actor_id = cast_data.get("targetID")

            if self._has_source_id and (cast_actor_id != self.source_id):
                continue

            # Add the Cast Object
            cast = Cast()
            cast.spell_id = cast_data.get("abilityGameID")
            cast.spell_id = WowSpell.resolve_spell_id(cast.spell_id)
            cast.timestamp = cast_data.get("timestamp", 0) - fight_start
            cast.duration = cast_data.get("duration")
            if cast.duration:
                cast.duration *= 0.001

            # we check if the buff was applied before..
            if cast_type == "removebuff":
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
        self.casts = utils.uniqify(self.casts, key=lambda cast: (cast.spell_id, math.floor(cast.timestamp / 1000)))
        self.casts = list(self.casts) # `utils.uniqify` returns dict values, which mongoengine doesn't like

        # make sure casts are sorted correctly
        # avoids weird UI overlaps, and just feels cleaner
        self.casts = sorted(self.casts, key=lambda cast: cast.timestamp)


class Player(BaseActor):
    """A PlayerCharater in a Fight (or report)."""

    source_id: int = me.IntField(primary_key=True)
    name: str = me.StringField(max_length=12) # names can be max 12 chars
    total: int = me.IntField(default=0)

    class_slug: str = me.StringField()
    spec_slug: str = me.StringField(required=True)

    covenant_id: int = me.IntField(default=0)
    soulbind_id: int = me.IntField(default=0)

    deaths = me.ListField(me.DictField())

    def __str__(self):
        return f"Player(id={self.source_id} name={self.name} spec={self.spec})"

    def summary(self):

        class_slug = self.class_slug or self.spec_slug.split("-")[0]

        return {
            "name": self.name,
            "source_id": self.source_id,
            "class": class_slug,

            "spec": self.spec_slug,
            "role": self.spec.role.code if self.spec else "",
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

    ############################################################################
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

    def get_sub_query(self) -> str:
        """Get the Query for fetch all relevant data for this player."""
        filters = []

        cast_query = self.get_cast_query(self.spec.all_spells)
        filters.append(cast_query)

        buffs_query = self.get_buff_query(self.spec.all_buffs)
        filters.append(buffs_query)

        # combine all filters
        filters = [f for f in filters if f]   # filter the filters
        filters = [f"({f})" for f in filters] # wrap each filter into bracers
        filters = [" or ".join(filters)]

        queries_combined = " and ".join(filters)
        return f"({queries_combined})"

    def process_query_result(self, query_result):
        super().process_query_result(query_result)

        # for spec rankings we don't know the source ID upfront..
        # but we can fill that gap here
        if not self._has_source_id:
            casts = utils.get_nested_value(query_result, "report", "events", "data") or []
            for cast in casts:
                if cast.get("type") == "cast":
                    self.source_id = cast.get("sourceID")
                    break

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
