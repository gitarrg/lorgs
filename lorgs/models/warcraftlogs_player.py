
# IMPORT STANRD LIBRARIES
import typing

# IMPORT LOCAL LIBRARIES
from lorgs.clients import wcl
from lorgs.models.warcraftlogs_actor import BaseActor
from lorgs.models.wow_spec import WowSpec
from lorgs.models.wow_spell import EventSource, WowSpell


class Player(BaseActor):
    """A PlayerCharater in a Fight (or report)."""

    name: str = ""
    class_slug: str = ""
    spec_slug: str = ""

    total: float = 0

    deaths: list = []
    resurrects: list = []

    def __str__(self) -> str:
        return f"Player(id={self.source_id} name={self.name} spec={self.spec})"

    def summary(self) -> dict[str, typing.Any]:
        return {
            "name": self.name,
            "source_id": self.source_id,
            "class": self.class_slug,

            "spec": self.spec_slug,
            "role": self.spec.role.code if self.spec else "",
        }

    def as_dict(self) -> dict[str, typing.Any]:
        return {
            **self.summary(),
            "total": int(self.total),
            "casts": [cast.dict() for cast in self.casts],
            "deaths": self.deaths,
            "resurrects": self.resurrects,
        }

    ##########################
    # Attributes
    #
    @property
    def spec(self) -> WowSpec:
        return WowSpec.get(full_name_slug=self.spec_slug)

    ############################################################################
    # Query
    #
    def get_cast_query(self, spells: list[WowSpell]):
        cast_query = super().get_cast_query(spells=spells)
        if cast_query and self.name:
            cast_query = f"source.name='{self.name}' and {cast_query}"
        return cast_query

    def get_buff_query(self, spells: list[WowSpell]):
        buffs_query = super().get_buff_query(spells=spells)
        if buffs_query and self.name:
            buffs_query = f"target.name='{self.name}' and {buffs_query}"
        return buffs_query

    def get_debuff_query(self, spells: list[WowSpell]):
        debuffs_query = super().get_debuff_query(spells=spells)
        if debuffs_query and self.name:
            debuffs_query = f"source.name='{self.name}' and {debuffs_query}"
        return debuffs_query

    def get_event_query(self, spells: list[WowSpell]):

        # 1) spells used by the player
        player_query = ""
        player_spells = [e for e in spells if e.source == EventSource.PLAYER]
        if player_spells:
            player_query = super().get_event_query(spells=player_spells)
            if player_query and self.name:
                player_query = f"source.name='{self.name}' and {player_query}"

        return player_query or ""

    def get_sub_query(self) -> str:
        """Get the Query for fetch all relevant data for this player."""

        filters = [
            self.get_event_query(self.spec.all_events),
            self.get_cast_query(self.spec.all_spells),
            self.get_buff_query(self.spec.all_buffs),
            self.get_debuff_query(self.spec.all_debuffs),
        ]

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

    def process_death_events(self, death_events: list[wcl.DeathEvent]):
        """Add the Death Events the the Players.

        Args:
            death_events[list[dict]]

        """

        # TODO: add during model validation?
        # ABILITY_OVERWRITES = {}
        # ABILITY_OVERWRITES[1] = {"name": "Melee", "guid": 260421, "abilityIcon": "ability_meleedamage.jpg"}
        # ABILITY_OVERWRITES[3] = {"name": "Fall Damage"}

        for death_event in death_events:
            target_id = death_event.id
            if self._has_source_id and (target_id != self.source_id):
                continue

            death_ability = death_event.ability
            # death_ability_id = death_ability.guid
            # death_ability = ABILITY_OVERWRITES.get(death_ability_id) or death_ability

            death_data = {
                "ts": death_event.deathTime,
                "spell_name": death_ability.name,
                "spell_icon": death_ability.abilityIcon,
            }
            self.deaths.append(death_data)

    def process_event_resurrect(self, event: "wcl.ReportEvent"):
        fight_start = self.fight.start_time_rel if self.fight else 0

        data: dict[str, typing.Any] = {}
        data["ts"] = event.timestamp - fight_start

        spell_id = event.abilityGameID
        spell = WowSpell.get(spell_id=spell_id)
        if spell:
            data["spell_name"] = spell.name
            data["spell_icon"] = spell.icon

        # Look for the Source ID
        source_id = event.sourceID
        if self.fight and self.fight.report:
            source_player = self.fight.report.players.get(str(source_id))
            if source_player:
                data["source_name"] = source_player.name
                data["source_class"] = source_player.class_slug

        self.resurrects.append(data)

    def process_event(self, event: "wcl.ReportEvent"):
        super().process_event(event)

        # Ankh doesn't shows as a regular spell
        spell_id = event.abilityGameID
        if spell_id in (21169,): # Ankh
            event.type = "resurrect"

        if event.type == "resurrect":
            self.process_event_resurrect(event)
