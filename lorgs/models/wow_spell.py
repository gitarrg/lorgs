"""A Spell/Ability in the Game."""

# IMPORT LOCAL LIBRARIES
from lorgs.models import base


class WowSpell(base.Model):
    """Container to define a spell."""

    # TODO: those should be constants somewhere
    TYPE_RAID = "raid"
    TYPE_PERSONAL = "personal"
    TYPE_EXTERNAL = "external"

    TYPE_BUFFS = "other-buffs"
    TYPE_TRINKET = "other-trinkets"
    TYPE_POTION = "other-potions"

    # tags to indicate special properties
    TAG_DYNAMIC_CD = "dynamic_cd"


    def __init__(self, spell_id: int, cooldown: int = 0, duration: int = 0, show: bool = True, **kwargs):
        self.spell_id = spell_id
        self.cooldown = cooldown
        self.duration = duration

        self.icon = kwargs.get("icon") or ""
        self.name = kwargs.get("name") or ""
        self.show = show
        self.color = kwargs.get("color") or ""

        # str: type/category of spell
        self.spell_type = kwargs.get("spell_type") or ""

        # list(str): tags to indicate special properties
        self.tags = kwargs.get("tags") or []

        """str: info used for the wowhead tooltips."""
        self.wowhead_data = kwargs.get("wowhead_data") or  f"spell={self.spell_id}"

    def __repr__(self):
        return f"<Spell({self.spell_id}, cd={self.cooldown})>"

    def is_item_spell(self):
        """bool: true if this spell from an item."""
        return self.spell_type in (self.TYPE_TRINKET, self.TYPE_POTION)

    def is_healing_cooldown(self):
        """bool: true if a spell is what we call a healer cooldown."""
        if self.is_item_spell():
            return False
        if self.spell_type in (self.TYPE_PERSONAL, ):
            return False
        return True

    ##########################
    # Methods
    #
    def as_dict(self):
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
