"""Models for Classes, Specs, Spells and Roles."""

# IMPORT LOCAL LIBRARIES
from lorgs import utils
from lorgs.models import base


class WowRole(base.Model):
    """A role like Tank, Healer, DPS."""

    def __init__(self, code: str, name: str, sort_index=99):
        self.code = code
        self.name = name
        self.specs = []

        self.icon_name = f"roles/{self.name.lower()}.jpg"
        self.sort_index = sort_index

    def __repr__(self):
        return f"<Role({self.name})>"

    def __lt__(self, other):
        return self.sort_index < other.sort_index

    @property
    def metric(self):
        """str: the preferred metric. aka: dps for all. hps for healers."""
        return "hps" if self.code == "heal" else "dps"


class WowClass(base.Model):
    """A playable class in wow."""

    def __init__(self, name: str, color: str):
        self.name = name
        self.color = color
        self.specs = []

        self.name_slug_cap = self.name.replace(" ", "")
        self.name_slug = utils.slug(self.name)

        #: bool: flag for the trinkets/potions groups
        self.is_other = self.name.lower() == "other"

    def __repr__(self):
        return f"<Class(name='{self.name}')>"

    def add_spec(self, *args, **kwargs):
        kwargs["wow_class"] = self
        spec = WowSpec(*args, **kwargs)
        self.specs.append(spec)
        return spec

    def add_spell(self, **kwargs):
        # kwargs.setdefault("color", self.color)
        for spec in self.specs:
            spec.add_spell(**kwargs)


class WowSpec(base.Model):
    """docstring for Spec"""

    def __init__(self, name, wow_class, role=None, short_name: str = ""):
        super().__init__()
        # self.id = 0
        self.name = name
        self.wow_class = wow_class
        self.role = role
        self.short_name = short_name or self.name
        # self.spells = {}

        # used for sorting
        # role_order = {"tank": 0, "heal": 1, "rdps": 2, "mdps": 3, "other": 4}
        # self.role_index = role_order.get(self.role, 99)

        # bool: is this spec is currently supported
        self.supported = True

        # Generate some names
        self.name_slug = utils.slug(self.name)
        self.name_slug_cap = self.name.replace(" ", "")
        self.full_name = f"{self.name} {self.wow_class.name}"
        self.full_name_slug = f"{self.wow_class.name_slug}-{self.name_slug}"
        # self.class_name = self.class_.name
        # self.short_name = self.name # to be overwritten
        # slugified names
        # self.class_name_slug = self.class_.name_slug

        self.icon_name = f"specs/{self.full_name_slug}.jpg"

        self.spells = []

    def __repr__(self):
        return f"<Spec({self.full_name})>"

    def __lt__(self, other):
        return (self.role, self.name) < (other.role, other.name)

    def add_spell(self, **kwargs):
        # kwargs.setdefault("color", self.wow_class.color)

        kwargs["group"] = kwargs.get("group") or self
        kwargs.setdefault("spec", self)
        spell = WowSpell(**kwargs)
        self.spells.append(spell)
        return spell


class WowSpell(base.Model):
    """Container to define a spell."""

    # yoink
    ICON_ROOT = "https://wow.zamimg.com/images/wow/icons/medium"

    def __init__(self, spell_id, spec=None, duration=0, cooldown=0, show=True, group=None, **kwargs):
        super().__init__()

        # game info
        self.spell_id = spell_id
        self.duration = duration
        self.cooldown = cooldown

        # display info
        self.group = group
        self.show = show
        self.color = kwargs.get("color") or (group and group.wow_class.color)

        self.spec = spec

        # info from query
        self.icon_name = kwargs.get("icon_name") or ""
        self.spell_name = kwargs.get("spell_name") or ""

        # the data for the wowhead tooltip.
        # pregenerated, so we can overwrite it, eg.: for trinkets
        self.wowhead_data = kwargs.get("wowhead_data") or f"spell={self.spell_id}"

    def __repr__(self):
        return f"<Spell({self.spell_id}, cd={self.cooldown})>"

    def __getstate__(self):

        print("saving spell", self)

        return {
            "spell_id": self.spell_id
        }

        # capture what is normally pickled
        state = self.__dict__.copy()
        # replace the `value` key (now an EnumValue instance), with it's index:
        # state["test"] = state['value'].index
        # what we return here will be stored in the pickle
        return state

    def __setstate__(self, newstate):
        # re-create the EnumState instance based on the stored index
        raise NotImplementedError

        print("loading spell", newstate)

        spell_id = newstate.get("spell_id")
        return self.get(spell_id=spell_id)

        # self.__dict__.update(newstate)

    def as_dict(self):

        return {
            "spell_id": self.spell_id,
            "spell_name": self.spell_name,
            "duration": self.duration,
            "cooldown": self.cooldown,

            # display attributes
            "icon_name": self.icon_name,
            "color": self.color,
            "show": self.show,
        }

    @property
    def icon_path(self):
        return f"{self.ICON_ROOT}/{self.icon_name}"
