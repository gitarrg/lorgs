
# IMPORT STANRD LIBRARIES
import textwrap

# IMPORT THIRD PARTY LIBRARIES
import mongoengine as me

# IMPORT LOCAL LIBRARIES
from lorgs import utils
from lorgs.logger import logger
from lorgs.models import warcraftlogs_base
from lorgs.models.encounters import RaidBoss
from lorgs.models.specs import WowSpec
from lorgs.models.specs import WowSpell
from lorgs.models.specs import WowCovenant


class Cast(me.EmbeddedDocument):
    """docstring for Cast"""

    timestamp = me.IntField()
    spell_id = me.IntField()
    duration = me.IntField()

    def __str__(self):
        time_fmt = utils.format_time(self.timestamp)
        return f"Cast({self.spell_id}, at={time_fmt})"

    def as_dict(self):
        return {
            "ts": self.timestamp,
            "id": self.spell_id,
        }

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
    def spells_used(self):
        """Only the spells this player has used in this fight."""
        used_spell_ids = set(cast.spell_id for cast in self.casts)
        return [spell for spell in self.spec.spells if spell.spell_id in used_spell_ids]

    @property
    def lifetime(self):
        return self.fight.duration

    @property
    def _has_source_id(self):
        return self.source_id >= 0

    #################################
    # Query
    #
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

        for cast_data in casts_data:

            # TODO: fetch source_id's?
            if self._has_source_id and cast_data.get("sourceID") != self.source_id:
                continue

            cast = Cast()
            cast.spell_id = cast_data["abilityGameID"]
            cast.timestamp = cast_data["timestamp"] - self.fight.start_time_rel
            self.casts.append(cast)

            # if this is the only player in the dataset --> fetch the source ID
            # if self.source_id <= 0 and len(self.fight.players) == 1:
            #     self.source_id = cast_data.get("sourceID")

        # Filter out same event at the same time (eg.: raid wide debuff apply)
        self.casts = utils.uniqify(self.casts, key=lambda cast: (cast.spell_id, cast.timestamp))
        self.casts = list(self.casts) # `utils.uniqify` returns dict values, which mongoengine doesn't like


class Player(BaseActor):
    """A PlayerCharater in a Fight."""

    source_id = me.IntField(primary_key=True) # TODO: rename?
    name = me.StringField(max_length=12) # names can be max 12 chars
    total = me.FloatField()
    spec_slug = me.StringField(required=True)

    covenant_id = me.IntField()
    soulbind_id = me.IntField()

    deaths = me.ListField(me.DictField())

    def __str__(self):
        return f"Player(id={self.source_id} name={self.name} spec={self.spec})" # casts={len(self.casts)})"

    def as_dict(self):
        return {
            "name": self.name,
            "total": int(self.total),

            "source_id": self.source_id,
            "covenant": self.covenant.name_slug,
            "casts": [cast.as_dict() for cast in self.casts],

            "spec": self.spec_slug,
            "role": self.spec.role.code,
            "class": self.spec.wow_class.name_slug,
        }

    ##########################
    # Attributes
    #
    @property
    def spec(self):
        return WowSpec.get(full_name_slug=self.spec_slug)

    @property
    def covenant(self):
        return WowCovenant.get(id=self.covenant_id or 0)

    @property
    def report_url(self):
        if self._has_source_id:
            return f"{self.fight.report_url}&source={self.source_id}"
        return f"{self.fight.report_url}"

    @property
    def lifetime(self):
        if self.deaths:
            return self.deaths[-1].get("deathTime", 0)

        return self.fight.duration

    #################################
    # Query
    #

    def get_sub_query(self, filters=None):
        """Not needed/tested...

        TODO:
            - add filter by source_id if preset

        """
        filters = filters or []

        if self.name:
            filters += [f"source.name='{self.name}'"]

        # TODO: combine with "Fight._build_cast_query"
        spell_ids = [spell.spell_id for spell in self.spec.spells]
        spell_ids = sorted(list(set(spell_ids)))
        spell_ids = ",".join(str(spell_id) for spell_id in spell_ids)

        filters += [f"type='cast' and ability.id in ({spell_ids})"]
        filters = " and ".join(filters)

        return f"events({self.fight.table_query_args}, filterExpression: \"{filters}\") {{data}}"

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

    @property
    def raid_boss(self):
        return RaidBoss.get(id=self.boss_id)

    @property
    def spec(self):
        # dummy for now, to make the html templates work
        return {}  # TODO

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

    def as_dict(self):
        d = self.raid_boss.as_dict()
        d["zone"] = self.raid_boss.zone.as_dict()
        d["casts"] = [cast.as_dict() for cast in self.casts]
        return d

    ##########################
    # Methods
    #
    def get_sub_query(self, filters=None):
        filters = filters or []

        for event in self.raid_boss.events:

            # get all event parts
            parts = []
            if event.get("event_type"):
                parts.append("type='{event_type}'")
            if event.get("spell_id"):
                parts.append("ability.id={spell_id}")
            if event.get("extra_filter"):
                parts.append("{extra_filter}")

            # combine filter
            event_filter = " and ".join(parts)
            event_filter = f"({event_filter})"
            event_filter = event_filter.format(**event)

            # add filter to list
            filters.append(event_filter)

        filters = " or ".join(filters)

        if not filters:
            return ""

        return f"events({self.fight.table_query_args}, filterExpression: \"{filters}\") {{data}}"


    def process_query_result(self, query_result):
        """Process the result of a casts-query to create Cast objects."""
        super().process_query_result(query_result)


        for event in self.raid_boss.events:

            # skip events without explicit until-statement
            if not event.get("until"):
                continue

            until_event = event.get("until")
            event_spell = event.get("spell_id")
            end_spell_id = until_event.get("spell_id")

            start_cast = None
            end_casts = []
            for cast in self.casts:

                # look for the start event
                if not start_cast and cast.spell_id == event_spell:
                    start_cast = cast
                    continue

                # look for the ending event
                if start_cast and cast.spell_id == end_spell_id:
                    start_cast.end_time = cast.timestamp
                    start_cast = None
                    end_casts.append(cast)

            # end casts should not show up on their own
            self.casts = [cast for cast in self.casts if cast not in end_casts]
