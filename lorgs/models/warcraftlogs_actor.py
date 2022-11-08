# IMPORT STANRD LIBRARIES
import abc
import textwrap
import typing

# IMPORT THIRD PARTY LIBRARIES
import pydantic

# IMPORT LOCAL LIBRARIES
from lorgs import events
from lorgs import utils
from lorgs.clients import wcl
from lorgs.logger import logger
from lorgs.models import warcraftlogs_base
from lorgs.models.warcraftlogs_cast import Cast
from lorgs.models.wow_spell import WowSpell

if typing.TYPE_CHECKING:
    from lorgs.models.wow_actor import WowActor
    from lorgs.models.warcraftlogs_fight import Fight


def build_aura_query(spells: list[WowSpell], event_types: list[str]) -> str:
    """Build a query for Aura (buffs, debuffs).

    Args:
        spells(list[WowSpell]): List of spells to query.
        event_types(list[str]): List of event types to query (eg.: "applybuff", appldebuff"")

    TODO:
        * Check if duration is set. Only query auraremove if required.
    """
    if not spells:
        return ""
    spell_ids = WowSpell.spell_ids_str(spells)

    event_types = [f"'{event}'" for event in event_types]  # wrap each into single quotes
    event_types_combined = ",".join(event_types)

    return f"type in ({event_types_combined}) and ability.id in ({spell_ids})"


class BaseActor(pydantic.BaseModel, warcraftlogs_base.wclclient_mixin):
    """Base Class for any Actor in a Fight.

    these are usually either Players or NPC/Bosses

    """

    source_id: int = -1
    casts: list[Cast] = []

    fight: typing.Optional["Fight"] = pydantic.Field(exclude=True, default=None, repr=False)

    ############################################################################
    #
    # Attributes
    #
    ############################################################################

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

    @abc.abstractmethod
    def get_actor_type(self) -> "WowActor":
        """Get the Type of Actor."""

    @property
    def actor_type(self) -> "WowActor":
        return self.get_actor_type()

    async def load(self, *args: typing.Any, **kwargs: typing.Any) -> None:
        await events.submit("actor.load.start", actor=self)
        try:
            await super().load(*args, **kwargs)
        except:
            await events.submit("actor.load.failed", actor=self)
            raise
        else:
            await events.submit("actor.load.done", actor=self)

    ############################################################################
    #
    # Query
    #
    ############################################################################

    def get_cast_query(self, spells: list[WowSpell]) -> str:
        if not spells:
            return ""

        spell_ids = WowSpell.spell_ids_str(spells)
        cast_filter = f"type='cast' and ability.id in ({spell_ids})"
        return cast_filter

    def get_buff_query(self, spells: list[WowSpell]):
        return build_aura_query(spells, ["applybuff", "removebuff"])

    def get_debuff_query(self, spells: list[WowSpell]):
        return build_aura_query(spells, ["applydebuff", "removedebuff"])

    def get_events_query(self, spells: list[WowSpell]) -> str:
        """Generate the Query based of the given Spells.

        Generates a very verbose:
        ```
            "(type='spellA.type' and ability.id=spellA.spell_id) or (type='spellB.type' and ability.id=spellB.spell_id)"
        ```

        Args:
            spells WowSpell[]: List of Spells

        Returns:
            str: The Query

        TODO:
            * group spells by event_type
        """
        if not spells:
            return ""

        spells += [e.until for e in spells if e.until]  # include until events
        parts = [f"(type='{spell.event_type}' and ability.id={spell.spell_id})" for spell in spells]
        return " or ".join(parts)

    @abc.abstractmethod
    def get_sub_query(self) -> str:
        return ""

    def get_query(self) -> str:
        if not self.fight:
            raise ValueError("missing fight")
        if not self.fight.report:
            raise ValueError("missing report")

        return textwrap.dedent(
            f"""\
            reportData
            {{
                report(code: "{self.fight.report.report_id}")
                {{
                    events({self.fight.table_query_args}, filterExpression: "{self.get_sub_query()}")
                        {{data}}
                }}
            }}
        """
        )

    ############################################################################
    #
    # Process
    #
    ############################################################################

    def process_event(self, event: wcl.ReportEvent) -> wcl.ReportEvent:
        """Hook to preprocess each Cast/Event

        Args:
            event (wcl.ReportEvent): The Event to be processed
        """
        return event

    def set_source_id_from_events(self, casts: list[wcl.ReportEvent], force=False):
        """Set the Source ID from the cast data.

        In some cases (eg.: data pulled from spec rankings) we don't know the source ID upfront..
        but we can fill that gap here
        """
        if force == False and self._has_source_id:
            return

        for cast in casts:
            if cast.type == "cast":
                self.source_id = cast.sourceID

            # return as soon as we have a value
            if self.source_id > 0:
                return

    def process_query_result(self, **query_data: typing.Any) -> None:
        """Process the result of a casts-query to create Cast objects."""
        query_data = query_data.get("reportData") or query_data
        report_data = wcl.ReportData(**query_data)
        casts_data = report_data.report.events

        if not casts_data:
            logger.warning("casts_data is empty")
            return

        ##############################
        # Pre Processing
        self.set_source_id_from_events(casts_data)

        ##############################
        # Main
        for cast_data in casts_data:
            cast_data = self.process_event(cast_data)

            # Some Types (eg.: Buffs) are tracked based on the target.
            # eg.: PowerInfusion shows on the Target, not the Priest.
            cast_actor_id = cast_data.sourceID
            if cast_data.type in ("applybuff", "removebuff", "resurrect"):
                cast_actor_id = cast_data.targetID

            # Skip if the Source ID doesn't match
            if self._has_source_id and (cast_actor_id != self.source_id):
                continue

            # create the cast object
            cast = Cast.from_report_event(cast_data)
            cast.timestamp -= self.fight.start_time_rel if self.fight else 0
            self.casts.append(cast)

        ##############################
        # Post Processing
        self.casts = Cast.process_until_events(self.casts)
        self.casts = Cast.process_auras(self.casts)

        # Filter out same event at the same time (eg.: raid wide debuff apply)
        self.casts = utils.uniqify(self.casts, key=lambda cast: (cast.spell_id, int(cast.timestamp / 1000)))

        # make sure casts are sorted correctly
        # avoids weird UI overlaps, and just feels cleaner
        self.casts = sorted(self.casts, key=lambda cast: cast.timestamp)
