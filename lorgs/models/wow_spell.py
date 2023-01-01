"""A Spell/Ability in the Game."""
from __future__ import annotations

# IMPORT STANDARD LIBRARIES
import typing

from lorgs import utils

# IMPORT LOCAL LIBRARIES
from lorgs.models import base


class SpellType:
    """Enum for Spell Types.

    Note: This is not a real enum, as there are many more types not listed here.
    eg.: each Clas / Spec / Boss also defines a type
    """

    RAID = "other-raid"
    PERSONAL = "personal"
    EXTERNAL = "external"

    BUFF = "other-buffs"
    HERO = "other-hero"
    TRINKET = "other-trinkets"
    POTION = "other-potions"


class SpellTag:
    """Tags to annotate special properties of a spell.

    a single spell may have multiple (or zero) tags.
    """

    DYNAMIC_CD = "dynamic_cd"
    """Hint for spells whichs cooldown is reduced dynamically. eg.: Salvation"""

    RAID_CD = "raid_cd"


class WowSpell(base.MemoryModel):
    """Container to define a spell."""

    spell_variations: typing.ClassVar[dict[int, int]] = {}
    """Map to track spell variations and their "master"-spells.
        `[key: id of the variation] = id of the "master"-spell`
    """

    spell_id: int
    cooldown: int = 0
    duration: int = 0
    icon: str = ""
    name: str = ""
    color: str = ""
    show: bool = True

    variations: list[int] = []
    """Spell IDs for Variants of the same Spell. Eg.: Glyphs or Talents sometimes change the Spell ID."""

    spell_type: str = ""
    """type/category of spell. This is usuals the class or spec name.
    But can also be things like "other-trinket" or "other-buffs" for Raid Buffs."""

    tags: list[str] = []
    """tags to indicate special properties. eg.: dynamic cooldown."""

    event_type: str = "cast"
    """type of event (eg.: "cast", "buff", debuff)."""

    wowhead_data: str = ""
    """Info used for the wowhead tooltips."""

    until: typing.Optional["WowSpell"] = None
    """Custom End-Event."""

    extra_filter: str = ""
    """Extra filter for the spell."""

    def post_init(self) -> None:
        self.wowhead_data = self.wowhead_data or f"spell={self.spell_id}"
        self.add_variations(*self.variations)
        return super().post_init()

    @staticmethod
    def spell_ids(spells: typing.List["WowSpell"]) -> typing.List[int]:
        """Converts a list of Spells to their spell_ids."""
        ids = []  # [spell.spell_id for spell in spells]
        for spell in spells:
            ids += [spell.spell_id] + spell.variations
        ids = sorted(list(set(ids)))
        return ids

    @classmethod
    def spell_ids_str(cls, spells: typing.List["WowSpell"]) -> str:
        """Converts a list of Spells into a string of spell ids.

        Used to construct queries

        Example:
            spell_ids_str([Spell100, Spell200, Spell300])
            >>> "100,200,300
        """
        spell_ids = cls.spell_ids(spells)
        return ",".join(str(spell_id) for spell_id in spell_ids)

    @classmethod
    def resolve_spell_id(cls, spell_id: int) -> int:
        """Resolve a Spell ID for a spell variation to its main-spell."""
        return cls.spell_variations.get(spell_id) or spell_id

    def __str__(self) -> str:
        return f"<Spell({self.spell_id}, name={self.name})>"

    def is_item_spell(self) -> bool:
        """True if this spell from an item."""
        return self.spell_type in (self.TYPE_TRINKET, self.TYPE_POTION)

    def is_healing_cooldown(self) -> bool:
        """True if a spell is what we call a healer cooldown."""
        if self.is_item_spell():
            return False
        if self.spell_type in (self.TYPE_PERSONAL,):
            return False
        return True

    ##########################
    # Methods
    #
    def as_dict(self) -> dict[str, typing.Any]:
        return {
            "spell_id": self.spell_id,
            "duration": self.duration,
            "cooldown": self.cooldown,
            "spell_type": self.spell_type,
            # display attributes
            "name": self.name,
            "icon": self.icon,
            "color": self.color,
            "show": self.show,
            "tooltip_info": self.wowhead_data,
            "tags": self.tags,
        }

    def add_variation(self, spell_id: int):
        """Add an additional spell ids for the "same" spell.

        eg.: glyphed versions of the spell
        or sometimes boss abiltieis use different spells in
        differnet phases for the same mechanic
        """
        self.variations.append(spell_id)
        self.spell_variations[spell_id] = self.spell_id

    def add_variations(self, *spell_ids: int):
        for spell_id in spell_ids:
            self.add_variation(spell_id)

    def expand_events(self) -> list["WowSpell"]:

        # dedicated "until-event"
        if self.until:
            return [self, self.until]

        # we have fixed duration --> we are fine
        if self.duration:
            return [self]

        # automatic mirror_events for buffs/debuffs
        if self.event_type in ("applybuff", "applydebuff"):
            event_type = self.event_type.replace("apply", "remove")
            end = WowSpell(spell_id=self.spell_id, event_type=event_type)
            return [self, end]

        return [self]


def build_spell_query(spells: list[WowSpell]) -> str:

    if not spells:
        return ""

    spells = utils.flatten([spell.expand_events() for spell in spells])

    queries: list[str] = []

    spells_by_type = utils.group_by(*spells, keyfunc=lambda spell: spell.event_type)
    for event_type, event_spells in spells_by_type.items():
        spell_ids = WowSpell.spell_ids_str(event_spells)
        event_query = f"type='{event_type}' and ability.id in ({spell_ids})"
        event_query = f"({event_query})"

        queries.append(event_query)

    return " or ".join(queries)
