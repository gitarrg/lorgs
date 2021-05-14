"""Models for Classes, Specs, Spells and Roles."""
# pylint: disable=no-member

import sqlalchemy as sa

# IMPORT LOCAL LIBRARIES
from lorgs import utils
from lorgs.models import base


class WowRole(base.Model):
    """A role like Tank, Healer, DPS."""

    def __init__(self, name, code=""):
        # self.id = id
        self.name = name
        self.code = code or name.lower()

        self.icon_name = f"roles/{self.name.lower()}.jpg"
        self.specs = []

    def __repr__(self):
        return f"<Role({self.name})>"

    def __lt__(self, other):
        return self.id < other.id

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


"""
class SpecSpells():

    __tablename__ = "spec_spells"

    spec_id = sa.Column(sa.Integer, sa.ForeignKey("wow_spec.id", ondelete="cascade"), primary_key=True)
    spell_id = sa.Column(sa.Integer, sa.ForeignKey("wow_spell.spell_id", ondelete="cascade"), primary_key=True)
    group_id = sa.Column(sa.Integer, sa.ForeignKey("wow_spec.id"))

    spec = sa.orm.relationship("WowSpec", foreign_keys=[spec_id], back_populates="spells", lazy="joined")
    spell = sa.orm.relationship("WowSpell", foreign_keys=[spell_id], back_populates="specs", lazy="joined")
    group = sa.orm.relationship("WowSpec", foreign_keys=[group_id], lazy="joined")

    def __repr__(self):
        return f"<SpecSpells(spell={self.spell_id}, group={self.group.name})>"
"""


class WowSpec(base.Model):
    """docstring for Spec"""

    def __init__(self, id, wow_class, name, role="dps", short_name=""):
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

        self.icon_name = f"specs/{self.full_name_slug}.jpg"


    def __repr__(self):
        return f"<Spec({self.full_name})>"

    def __lt__(self, other):
        return (self.role, self.name) < (other.role, other.name)

    ##########################
    # Methods
    #

    def add_spell(self, **kwargs):

        # if spell_id in [spell.spell_id for spell in self.spells]:
        #     return
        kwargs.setdefault("color", self.wow_class.color)
        kwargs.setdefault("group", self)
        # group = kwargs.pop("group", self)
        # spell.color = kwargs.get("color")
        # kwargs["group"] = kwargs.get("group") or self
        # kwargs.pop("group")
        # kwargs.pop("wowhead_data", "")  # TODO
        # kwargs.pop("wowhead_data", "")  # TODO
        # spec  = kwargs.get("spec") or self
        # kwargs["spec_id"] = spec.name
        # spell_id = kwargs["spell_id"]
        spell = WowSpell(**kwargs)
        self.spells.append(spell)
        """
        if not spell:
            spell = WowSpell(spell_id=spell_id, **kwargs)
            # db.session.add(spell)

        ss = SpecSpells()
        ss.spec = self
        ss.group = group
        ss.spell = spell

        self.spells.append(ss)
        """
        return spell


class WowSpell(base.Model):
    """Container to define a spell."""

    # yoink
    ICON_ROOT = "https://wow.zamimg.com/images/wow/icons/medium"

    def __init__(self, spell_id: int, cooldown: int = 0, duration: int = 0, **kwargs):
        super().__init__()

        self.spell_id = spell_id
        self.cooldown = cooldown
        self.duration = duration

        self.icon_name = ""
        self.spell_name = ""
        self.show = True
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
        """str: url to the image path."""
        # for overwrites with custom images
        if self.icon_name.startswith("/"):
            return self.icon_name

        return f"{self.ICON_ROOT}/{self.icon_name}"
