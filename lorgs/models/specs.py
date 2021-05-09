"""Models for Classes, Specs, Spells and Roles."""
# pylint: disable=no-member

import sqlalchemy as sa

# IMPORT LOCAL LIBRARIES
from lorgs import utils
from lorgs.models import base
from lorgs import db


class WowRole(db.Base, base.IconPathMixin):
    """A role like Tank, Healer, DPS."""

    __tablename__ = "wow_role"

    id = sa.Column(sa.Integer(), primary_key=True)
    code = sa.Column(sa.String(4))
    name = sa.Column(sa.String(8))

    specs = sa.orm.relationship("WowSpec")

    __mapper_args__ = {
        "order_by" : id
    }

    @sa.orm.reconstructor
    def init_on_load(self):
        self.icon_name = f"roles/{self.name.lower()}.jpg"
        # self.code = code
        # self.name = name
        # self.specs = []
        # self.sort_index = sort_index

    def __repr__(self):
        return f"<Role({self.name})>"

    def __lt__(self, other):
        return self.id < other.id

    @property
    def metric(self):
        """str: the preferred metric. aka: dps for all. hps for healers."""
        return "hps" if self.code == "heal" else "dps"


class WowClass(db.Base):
    """A playable class in wow."""

    __tablename__ = "wow_class"

    id = sa.Column(sa.Integer(), primary_key=True, autoincrement=False)
    name = sa.Column(sa.String(16))
    color = sa.Column(sa.String(16))

    specs = sa.orm.relationship("WowSpec", back_populates="wow_class", lazy="joined")

    def __repr__(self):
        return f"<Class(name='{self.name}')>"

    @property
    def name_slug_cap(self):
        return self.name.replace(" ", "")

    @property
    def name_slug(self):
        return utils.slug(self.name)

    @property
    def is_other(self):
        #: bool: flag for the trinkets/potions groups
        return self.name.lower() == "other"

    def add_spell(self, **kwargs):
        # kwargs.setdefault("color", self.color)
        # kwargs.setdefault("group", self)
        for spec in self.specs:
            spec.add_spell(**kwargs)


class SpecSpells(db.Base):

    __tablename__ = "spec_spells"

    spec_id = sa.Column(sa.Integer, sa.ForeignKey("wow_spec.id", ondelete="cascade"), primary_key=True)
    spell_id = sa.Column(sa.Integer, sa.ForeignKey("wow_spell.spell_id", ondelete="cascade"), primary_key=True)
    group_id = sa.Column(sa.Integer, sa.ForeignKey("wow_spec.id"))

    spec = sa.orm.relationship("WowSpec", foreign_keys=[spec_id], back_populates="spells", lazy="joined")
    spell = sa.orm.relationship("WowSpell", foreign_keys=[spell_id], back_populates="specs", lazy="joined")
    group = sa.orm.relationship("WowSpec", foreign_keys=[group_id], lazy="joined")


class WowSpec(db.Base, base.IconPathMixin):
    """docstring for Spec"""

    __tablename__ = "wow_spec"

    id = sa.Column(sa.Integer(), primary_key=True, autoincrement=False)
    name = sa.Column(sa.String(16))
    short_name = sa.Column(sa.String(16))

    role = sa.orm.relationship("WowRole", back_populates="specs", lazy="joined")
    role_id = sa.Column(sa.Integer, sa.ForeignKey("wow_role.id"))

    supported = sa.Column(sa.Boolean, default=True)

    wow_class = sa.orm.relationship("WowClass", back_populates="specs", lazy="joined")
    wow_class_id = sa.Column(sa.Integer, sa.ForeignKey("wow_class.id", ondelete="cascade"))

    spells = sa.orm.relationship("SpecSpells", foreign_keys="SpecSpells.spec_id", back_populates="spec")

    def __repr__(self):
        return f"<Spec({self.full_name})>"

    def __lt__(self, other):
        return (self.role, self.name) < (other.role, other.name)

    def add_spell(self, spell_id, **kwargs):

        if spell_id in [spell.spell_id for spell in self.spells]:
            return

        kwargs.setdefault("color", self.wow_class.color)
        group = kwargs.pop("group", self)

        # spell.color = kwargs.get("color")
        # kwargs["group"] = kwargs.get("group") or self
        # kwargs.pop("group")
        # kwargs.pop("wowhead_data", "")  # TODO
        # kwargs.pop("wowhead_data", "")  # TODO
        # spec  = kwargs.get("spec") or self
        # kwargs["spec_id"] = spec.name

        # spell_id = kwargs["spell_id"]

        spell = WowSpell.query.get(spell_id)
        if not spell:
            spell = WowSpell(spell_id=spell_id, **kwargs)
            # db.session.add(spell)

        ss = SpecSpells()
        ss.spec = self
        ss.group = group
        ss.spell = spell

        self.spells.append(ss)
        return spell

   # Generate some names
    name_short     = property(lambda self: self.short_name or self.name)
    name_slug      = property(lambda self: utils.slug(self.name))
    name_slug_cap  = property(lambda self: self.name.replace(" ", ""))
    full_name      = property(lambda self: f"{self.name} {self.wow_class.name}")
    full_name_slug = property(lambda self: f"{self.wow_class.name_slug}-{self.name_slug}")
    icon_name      = property(lambda self: f"specs/{self.full_name_slug}.jpg")


class WowSpell(db.Base):
    """Container to define a spell."""

    __tablename__ = "wow_spell"

    spell_id = sa.Column(sa.Integer(), primary_key=True, autoincrement=False)
    spell_name = sa.Column(sa.String(64))
    wowhead_data = sa.Column(sa.String(128))
    icon_name = sa.Column(sa.String(128))
    duration = sa.Column(sa.Integer(), default=0)
    cooldown = sa.Column(sa.Integer(), default=0)

    # group = "todo"
    # group = {"class_name_slug": "paladin"} # TODO!
    color = sa.Column(sa.String(32))
    show = sa.Column(sa.Boolean(), default=True)

    specs = sa.orm.relationship("SpecSpells", back_populates="spell", lazy="joined")

    # group_id = db.Column(db.Integer, db.ForeignKey(WowSpec.id))
    # group = sqlalchemy.orm.relationship("WowSpec", foreign_keys=group_id, lazy="joined")

    # group = db.Column(db.String(128))
    # group = "todo"

    # show = True
    # wow_class = sqlalchemy.orm.relationship("WowClass", back_populates="specs")
    # wow_class_id = db.Column(db.Integer, db.ForeignKey("wow_class.id"))

    # yoink
    ICON_ROOT = "https://wow.zamimg.com/images/wow/icons/medium"

    """
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
    """

    def __repr__(self):
        return f"<Spell({self.spell_id}, cd={self.cooldown})>"

    """
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
    """

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
