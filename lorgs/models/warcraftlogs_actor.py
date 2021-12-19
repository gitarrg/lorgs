
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

    @staticmethod
    def _build_buff_query(spells: typing.List[WowSpell], event_types: typing.List[str]):
        if not spells:
            return ""
        spell_ids = WowSpell.spell_ids_str(spells)

        event_types = [f"'{event}'" for event in event_types] # wrap each into single quotes
        event_types_combined = ",".join(event_types)

        return f"type in ({event_types_combined}) and ability.id in ({spell_ids})"

    @classmethod
    def get_buff_query(cls, spells: typing.List[WowSpell]):
        return cls._build_buff_query(spells, ["applybuff", "removebuff"])

    @classmethod
    def get_debuff_query(cls, spells: typing.List[WowSpell]):
        return cls._build_buff_query(spells, ["applydebuff", "removedebuff"])

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

    def process_event(self, event):
        pass

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

        # track buffs/debuff: spell id -> start cast
        active_buffs: typing.Dict[int, Cast] = {}

        fight_start = self.fight.start_time_rel if self.fight else 0

        for cast_data in casts_data:
            self.process_event(cast_data)

            cast_type: str = cast_data.get("type") or "unknown"

            cast_actor_id = cast_data.get("sourceID")
            if cast_type in ("applybuff", "removebuff", "resurrect"):
                cast_actor_id = cast_data.get("targetID")

            if self._has_source_id and (cast_actor_id != self.source_id):
                continue


            # resurrect are dealt with in `process_event`
            if cast_type == "resurrect":
                continue

            # Create the Cast Object
            cast = Cast()
            cast.spell_id = cast_data.get("abilityGameID")
            cast.spell_id = WowSpell.resolve_spell_id(cast.spell_id)
            cast.timestamp = cast_data.get("timestamp", 0) - fight_start
            cast.duration = cast_data.get("duration")

            if cast_type in ("cast"):
                cast.stacks = 1

            # new buff, or buff stack
            if cast_type in ("applybuff", "applydebuff"):
                # check if the buff/debuff is already active.
                cast = active_buffs.get(cast.spell_id) or cast
                cast.stacks += 1

            if cast_type in ("removebuff", "removedebuff"):

                start_cast = active_buffs.get(cast.spell_id)

                # special case for buffs that are applied pre pull
                # meaning.. the buff was already present at the start of the fight,
                if not start_cast:
                    start_cast = cast
                    spell = WowSpell.get(spell_id=cast.spell_id) # get the duration from the spell defintion
                    start_cast.timestamp -= (spell.duration * 1000) # and calculate back the start time
                    continue

                start_cast.stacks -= 1

                # no stacks left --> buff/debuff ends
                if start_cast.stacks == 0:
                    start_cast.duration = (cast.timestamp - start_cast.timestamp)
                    start_cast.duration *= 0.001
                    active_buffs[cast.spell_id] = None

            if cast.stacks == 1:  # only add new buffs on their first application
                # track applied buffs
                active_buffs[cast.spell_id] = cast
                self.casts.append(cast)

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
    resurrects = me.ListField(me.DictField())

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
            "deaths": self.deaths,
            "resurrects": self.resurrects,
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
        if cast_query and self.name:
            cast_query = f"source.name='{self.name}' and {cast_query}"
        return cast_query

    def get_buff_query(self, spells=typing.List[WowSpell]):
        buffs_query = super().get_buff_query(spells=spells)
        if buffs_query and self.name:
            buffs_query = f"target.name='{self.name}' and {buffs_query}"
        return buffs_query

    def get_debuff_query(self, spells=typing.List[WowSpell]):
        debuffs_query = super().get_debuff_query(spells=spells)
        if debuffs_query and self.name:
            debuffs_query = f"source.name='{self.name}' and {debuffs_query}"
        return debuffs_query

    def get_sub_query(self) -> str:
        """Get the Query for fetch all relevant data for this player."""
        filters = []

        cast_query = self.get_cast_query(self.spec.all_spells)
        filters.append(cast_query)

        buffs_query = self.get_buff_query(self.spec.all_buffs)
        filters.append(buffs_query)

        debuff_query = self.get_debuff_query(self.spec.all_debuffs)
        filters.append(debuff_query)

        # Resurrections
        if self.name:
            resurect_query = f"target.name='{self.name}' and type='resurrect'"
            filters.append(resurect_query)

        # combine all filters
        filters = [f for f in filters if f]   # filter the filters
        filters = [f"({f})" for f in filters] # wrap each filter into bracers
        filters = [" or ".join(filters)]

        queries_combined = " and ".join(filters)
        return f"({queries_combined})"

    def process_death_events(self, death_events):
        """Add the Death Events the the Players.

        Args:
            death_events[list[dict]]

        """
        ABILITY_OVERWRITES = {}
        ABILITY_OVERWRITES[1] = {"name": "Melee", "guid": 260421, "abilityIcon": "ability_meleedamage.jpg"}
        ABILITY_OVERWRITES[3] = {"name": "Fall Damage"}

        for death_event in death_events:
            target_id = death_event.get("id", 0)
            if self._has_source_id and (target_id != self.source_id):
                continue

            death_ability = death_event.get("ability", {})
            death_ability_id = death_ability.get("guid", -1)
            death_ability = ABILITY_OVERWRITES.get(death_ability_id) or death_ability

            death_data = {}
            death_data["ts"] = death_event.get("deathTime", 0)
            death_data["spell_name"] = death_ability.get("name", "")
            death_data["spell_icon"] = death_ability.get("abilityIcon", "")
            self.deaths.append(death_data)
 
    def process_event_resurrect(self, event):
        fight_start = self.fight.start_time_rel if self.fight else 0

        data = {}
        data["ts"] = event.get("timestamp", 0) - fight_start

        spell_id = event.get("abilityGameID", -1)
        spell = WowSpell.get(spell_id=spell_id)
        if spell:
            data["spell_name"] = spell.name
            data["spell_icon"] = spell.icon

        source_id = event.get("sourceID", 0)
        source_player: Player = self.fight.report.players.get(str(source_id))
        if source_player:
            data["source_name"] = source_player.name
            data["source_class"] = source_player.class_slug

        self.resurrects.append(data)

    def process_event(self, event):
        super().process_event(event)

        # Ankh doesn't shows as a regular spell
        spell_id = event.get("abilityGameID", -1)
        if spell_id in (21169,): # Ankh
            event["type"] = "resurrect"

        event_type = event.get("type")

        if event_type == "resurrect":
            self.process_event_resurrect(event)

    def process_query_result(self, query_result):
        super().process_query_result(query_result)

        # for spec rankings we don't know the source ID upfront..
        # but we can fill that gap here
        if not self._has_source_id:
            casts = utils.get_nested_value(query_result, "report", "events", "data") or []
            for cast in casts:
                cast_type = cast.get("type")
                if cast_type == "cast":
                    self.source_id = cast.get("sourceID")
                    break
