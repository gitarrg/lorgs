"""Models for Classes, Specs, Spells and Roles."""

# IMPORT LOCAL LIBRARIES
from lorgs import utils
from lorgs.models import base


class WowRole(base.Model):
    """A role like Tank, Healer, DPS."""

    def __init__(self, name, code=""):
        self.name = name
        self.code = code or name.lower()

        self.icon = f"roles/{self.name.lower()}.jpg"
        self.specs = []

    def __repr__(self):
        return f"<Role({self.name})>"

    def __str__(self):
        return self.code

    def __lt__(self, other):
        return self.code < other.code

    @property
    def metric(self):
        """str: the preferred metric. aka: dps for all. hps for healers."""
        return "hps" if self.code == "heal" else "dps"


class WowClass(base.Model):
    """A playable class in wow."""

    def __init__(self, id: int, name: str, color: str=""):

        # int: class id, mostly used for sorting
        self.id = id
        self.name = name
        self.color = color
        self.specs = []

        self.name_slug_cap = self.name.replace(" ", "")
        self.name_slug = utils.slug(self.name)

        #: bool: flag for the trinkets/potions groups
        self.is_other = self.name.lower() == "other"

    def __repr__(self):
        return f"<Class(name='{self.name}')>"

    def __lt__(self, other):
        return self.id < other.id

    def add_spell(self, **kwargs):
        for spec in self.specs:
            spec.add_spell(**kwargs)


class WowSpec(base.Model):
    """docstring for Spec"""

    def __init__(self, wow_class: WowClass, name: str, role: WowRole, short_name: str = ""):
        super().__init__()
        self.name = name
        self.role = role

        self.spells = []

        self.wow_class = wow_class
        self.wow_class.specs.append(self)

        # bool: is this spec is currently supported
        self.supported = True

        # Generate some names
        self.full_name = f"{self.name} {self.wow_class.name}"
        self.short_name = short_name or self.name # to be overwritten

        # slugified names
        self.name_slug = utils.slug(self.name)
        self.full_name_slug = f"{self.wow_class.name_slug}-{self.name_slug}"

        # str: Spec Name without spaces, but still capCase.. eg.: "BeastMastery"
        self.name_slug_cap = self.name.replace(" ", "")

        self.icon = f"specs/{self.full_name_slug}.jpg"


    def __repr__(self):
        return f"<Spec({self.full_name})>"

    def __lt__(self, other):

        def sort_key(obj):
            return (obj.role, obj.wow_class, obj.name)

        return sort_key(self) < sort_key(other)

    def as_dict(self):

        return {
            "name": self.name,
            "name_slug": self.name_slug,
            "full_name": self.full_name,
            "full_name_slug": self.full_name_slug,
            "role": str(self.role),
        }

    ##########################
    # Methods
    #

    def add_spell(self, **kwargs):
        kwargs.setdefault("color", self.wow_class.color)
        kwargs.setdefault("group", self)

        spell = WowSpell(**kwargs)
        spell.spec = self
        self.spells.append(spell)

        return spell


class WowSpell(base.Model):
    """Container to define a spell."""

    # yoink
    ICON_ROOT = "https://wow.zamimg.com/images/wow/icons/medium"

    def __init__(self, spell_id: int, cooldown: int = 0, duration: int = 0, show: bool = True, **kwargs):
        self.spell_id = spell_id
        self.cooldown = cooldown
        self.duration = duration

        self.spec = None
        self.icon = kwargs.get("icon") or ""
        self.name = kwargs.get("name") or ""
        self.show = show
        self.color = kwargs.get("color") or ""
        self.group = kwargs.get("group")

        """str: info used for the wowhead tooltips."""
        self.wowhead_data = kwargs.get("wowhead_data") or  f"spell={self.spell_id}"

    def __repr__(self):
        return f"<Spell({self.spell_id}, cd={self.cooldown})>"

    ##########################
    # Methods
    #

    def as_dict(self):

        d = {
            "spell_id": self.spell_id,
            "duration": self.duration,
            "cooldown": self.cooldown,

            # display attributes
            "name": self.name,
            "icon": self.icon,
            "color": self.color,
            "show": self.show,
            "tooltip_info": self.wowhead_data,
        }

        d["group"] = self.group and self.group.as_dict() or {}

        return d

    @property
    def icon_path(self):
        """str: url to the image path."""
        # for overwrites with custom images
        if self.icon.startswith("/"):
            return self.icon
        return f"{self.ICON_ROOT}/{self.icon}"


class WowCovenant(base.Model):
    """Datacontainer for Covenants in the Game.

    Nightfae, Necrolord, Ventyr and Kyrian.

    """

    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.name_slug = utils.slug(self.name)
        self.icon = f"covenants/{self.name_slug}.jpg"

    def __repr__(self):
        return f"<Covenant({self.name})>"
