"""Models for Classes, Specs, Spells and Roles."""

# IMPORT LOCAL LIBRARIES
from lorgs import utils
from lorgs.models import base


class WowRole(base.Model):
    """A role like Tank, Healer, DPS."""

    def __init__(self, name, code=""):
        # self.id = id
        self.name = name
        self.code = code or name.lower()

        self.icon = f"roles/{self.name.lower()}.jpg"
        self.specs = []

    def __repr__(self):
        return f"<Role({self.name})>"

    def __lt__(self, other):
        return self.code < other.code

    @property
    def metric(self):
        """str: the preferred metric. aka: dps for all. hps for healers."""
        return "hps" if self.code == "heal" else "dps"


class WowClass(base.Model):
    """A playable class in wow."""

    def __init__(self, id, name, color=""):

        # self.id = id # TODO: check if needed?
        self.name = name
        self.color = color
        self.specs = []

        self.name_slug_cap = self.name.replace(" ", "")
        self.name_slug = utils.slug(self.name)

        #: bool: flag for the trinkets/potions groups
        self.is_other = self.name.lower() == "other"

    def __repr__(self):
        return f"<Class(name='{self.name}')>"

    def add_spell(self, **kwargs):
        for spec in self.specs:
            spec.add_spell(**kwargs)


class WowSpec(base.Model):
    """docstring for Spec"""

    def __init__(self, wow_class, name, role=None, short_name=""):
        super().__init__()
        # self.id = id
        self.name = name
        self.role = role

        self.spells = []

        self.wow_class = wow_class
        self.wow_class.specs.append(self)

        # used for sorting
        # role_order = {"tank": 0, "heal": 1, "rdps": 2, "mdps": 3, "other": 4}
        # self.role_index = role_order.get(self.role, 99)

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
        return (self.role, self.name) < (other.role, other.name)

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

    def __init__(self, spell_id: int, cooldown: int = 0, duration: int = 0, **kwargs):
        self.spell_id = spell_id
        self.cooldown = cooldown
        self.duration = duration

        self.spec = None
        self.icon = kwargs.get("icon") or ""
        self.name = kwargs.get("name") or ""
        self.show = kwargs.get("show") or True
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

        return {
            "spell_id": self.spell_id,
            "duration": self.duration,
            "cooldown": self.cooldown,

            # display attributes
            "name": self.name,
            "icon": self.icon,
            "color": self.color,
            "show": self.show,
        }

    @property
    def icon_path(self):
        """str: url to the image path."""
        # for overwrites with custom images
        if self.icon.startswith("/"):
            return self.icon
        return f"{self.ICON_ROOT}/{self.icon}"
