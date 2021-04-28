"""Models for Classes, Specs, Spells and Roles."""

# pylint: disable=too-few-public-methods

# IMPORT THIRD PARTY LIBRARIES
# import textwrap
import sqlalchemy
from sqlalchemy.ext.hybrid import hybrid_property #, hybrid_method
import flask

# IMPORT LOCAL LIBRARIES
from lorgs import utils
from lorgs.db import db
# from lorgs.logger import logger


###############################
# Constant Data

class WowRole(db.Model):
    """A role like Tank, Healer, DPS."""

    id = db.Column(db.Integer, primary_key=True) # mostly used for sort

    code = db.Column(db.String(4))
    name = db.Column(db.String(8))

    specs = sqlalchemy.orm.relationship("WowSpec", back_populates="role")

    def __repr__(self):
        return f"<Role({self.name})>"

    def __lt__(self, other):
        return self.id < other.id

    @property
    def img_path(self):
        filename = f"images/roles/{self.name.lower()}.jpg"
        return flask.url_for("static", filename=filename)

    @property
    def metric(self):
        """str: the preferred metric. aka: dps for all. hps for healers."""
        return "hps" if self.code == "heal" else "dps"


class WowClass(db.Model):
    """A playable class in wow."""

    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    name = db.Column(db.String(64))
    color = db.Column(db.String(32))

    specs = sqlalchemy.orm.relationship("WowSpec", back_populates="wow_class", cascade="all,save-update,delete")

    # def __init__(self, name):
    #     super().__init__()
        # self.name = name
        # self.specs = []
        # self.id = 0
        # self._all[self.name_slug] = self

    def __repr__(self):
        return f"<Class(name='{self.name}')>"

    def add_spell(self, spell_id, **kwargs):
        kwargs.setdefault("color", self.color)

        spell = WowSpell.get(spell_id=spell_id)
        spell.update(**kwargs)

        for spec in self.specs:
            spec.spells.append(spell)
        """
        """

    """
    @classmethod
    def get_by_name(cls, name):
        name = utils.slug(name)
        return cls._all.get(name)
    """

    @property
    def name_slug_cap(self):
        return self.name.replace(" ", "")

    @property
    def name_slug(self):
        return utils.slug(self.name)

    """
    def add_spec(self, **kwargs):
        spec = WowSpec(self, **kwargs)
        # spec.class_ = self
        self.specs.append(spec)
        return spec

    def get_spec(self, name):
        name = utils.slug(name)
        specs = {s.name_slug: s for s in self.specs}
        return specs.get(name)
    """


# table that stores which spells have access to which spells
spec_spells = db.Table( # pylint: disable=invalid-name
    "spec_spells",
    db.Column("spec_id", db.Integer, db.ForeignKey("wow_spec.id"), primary_key=True),
    db.Column("spell_id", db.Integer, db.ForeignKey("wow_spell.spell_id"), primary_key=True)
)


class WowSpec(db.Model):
    """docstring for Spec"""

    wow_class = sqlalchemy.orm.relationship("WowClass", back_populates="specs", lazy="joined")
    wow_class_id = db.Column(db.Integer, db.ForeignKey("wow_class.id", ondelete="cascade"), primary_key=True)

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)

    wcl_id = db.Column(db.Integer) # id used on warcraftlogs
    name = db.Column(db.String(64))
    color = db.Column(db.String(32))
    _short_name = db.Column("short_name", db.String(16))

    role = sqlalchemy.orm.relationship("WowRole", back_populates="specs")
    role_id = db.Column(db.Integer, db.ForeignKey("wow_role.id"))

    spells = sqlalchemy.orm.relationship("WowSpell", secondary=spec_spells, back_populates="specs")

    players = sqlalchemy.orm.relationship("Player", back_populates="spec")

    supported = db.Column(db.Boolean, default=True)

    """
    def __init__(self, class_, name, role="dps"):
        super().__init__()
        self.id = 0
        self.name = name
        self.role = role
        self.class_ = class_
        self.spells = {}

        # used for sorting
        role_order = {"tank": 0, "heal": 1, "rdps": 2, "mdps": 3, "other": 4}
        self.role_index = role_order.get(self.role, 99)

        # bool: is this spec is currently supported
        self.supported = True

        # Generate some names
        self.class_name = self.class_.name
        self.short_name = self.name # to be overwritten

        # slugified names

        self.class_name_slug = self.class_.name_slug

    """
    def __repr__(self):
        return f"<Spec({self.full_name})>"

    def __lt__(self, other):
        return (self.role, self.name) < (other.role, other.name)

    def as_dict(self):
        return {
            "name": self.name,
            "class": self.wow_class.name,
            "role": self.role.name,
        }

    @property
    def short_name(self):
        return self._short_name or self.name

    @short_name.setter
    def short_name(self, value):
        self._short_name = value

    @property
    def name_slug(self):
        return utils.slug(self.name)

    @property
    def name_slug_cap(self):
        """str: Spec Name without spaces, but still capCase.. eg.: BeastMastery."""
        return self.name.replace(" ", "")

    @property
    def full_name(self):
        return f"{self.name} {self.wow_class.name}"

    @hybrid_property
    def full_name_slug(self):
        return f"{self.wow_class.name_slug}-{self.name_slug}"

    """
    @property
    def _sort_tuple(self):
        return (self.role_index, self.name, self.full_name_slug)
    """

    def add_spell(self, spell_id, **kwargs):
        # kwargs["group"] = kwargs.get("group") or self
        kwargs.setdefault("color", self.wow_class.color)
        spell = WowSpell.get(spell_id=spell_id)
        spell.update(**kwargs)
        self.spells.append(spell)
        return spell
        # self.spells[spell.spell_id] = spell
        # return spell

    """
    @property
    def all_spells(self):
        return self.spells
        # return {**self.spells, **self.class_.spells}
    """

    @property
    def img_path(self):
        filename = f"images/specs/{self.full_name_slug}.jpg"
        return flask.url_for("static", filename=filename)


class WowSpell(db.Model):
    """Container to define a spell."""

    # def __new__(cls, spell_id, *args, **kwargs):
    #     """Create a new spell or reuse an instance if we already have that spell."""
    #     if spell_id not in cls._all:
    #         instance = super(WoWSpell, cls).__new__(cls)
    #         cls._all[spell_id] = instance
    #     return cls._all[spell_id]

    spell_id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    spell_name = db.Column(db.String(64))

    specs = sqlalchemy.orm.relationship("WowSpec", secondary=spec_spells, back_populates="spells", lazy="joined")
    # wow_spec_id = db.Column(db.Integer, db.ForeignKey("wow_spec.id", ondelete="cascade"))

    icon = db.Column(db.String(128))
    duration = db.Column(db.Integer, default=0)
    cooldown = db.Column(db.Integer, default=0)

    # group = "todo"
    # group = {"class_name_slug": "paladin"} # TODO!
    color = db.Column(db.String(32))
    show = db.Column(db.Boolean, default=True)
    # show = True

    # wow_class = sqlalchemy.orm.relationship("WowClass", back_populates="specs")
    # wow_class_id = db.Column(db.Integer, db.ForeignKey("wow_class.id"))

    """
    def __init__(self, spell_id, duration=0, cooldown=0, show=True, group=None, color=None):
        super().__init__()

        # game info
        self.spell_id = spell_id
        self.duration = duration
        self.cooldown = cooldown

        # display info
        self.group = group
        self.show = show
        self.color = color

        # info from query
        self.icon = ""
        self.name = ""
    """


    def __repr__(self):
        return f"<Spell({self.spell_id}, cd={self.cooldown})>"

    def __eq__(self, other):
        return self.spell_id == other.spell_id

    def __hash__(self):
        key = (self.spell_id, self.duration, self.cooldown, self.group)
        return hash(key)

    @property
    def group(self):  # TMP
        return self.specs[0]

