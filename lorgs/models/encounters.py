"""Models for Raids and RaidBosses."""
# pylint: disable=too-few-public-methods

# IMPORT LOCAL LIBRARIES
from lorgs import utils
from lorgs.models import base

from lorgs.models.specs import WowSpell


class RaidZone(base.Model):
    """A raid zone in the Game."""

    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.bosses = []

        self.name_slug = utils.slug(self.name, space="-")

    def __repr__(self):
        return f"<RaidZone(id={self.id} name={self.name})>"

    def as_dict(self):
        return {
            "id": self.id,
            "name": self.name,
        }

    def add_boss(self, **kwargs):
        boss = RaidBoss(zone=self, **kwargs)
        self.bosses.append(boss)
        return boss


class RaidBoss(base.Model):
    """A raid boss in the Game."""

    wow_class = {}

    def __init__(self, zone, id, name):
        self.id = id
        self.zone = zone
        self.name = name

        self.name_slug = utils.slug(self.name, space="-")
        self.icon = f"bosses/{self.zone.name_slug}/{self.name_slug}.jpg"

        # spells or buffs to track
        self.events = []

        # we track them as "spells" for now
        self.spells = []

    def __repr__(self):
        return f"<RaidBoss(id={self.id} name={self.name})>"

    def as_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            # "name_slug": self.name_slug,
        }

    ##########################
    # Methods
    #
    def add_event(self, **kwargs): # event_type, spell_id, name: str, icon: str, duration: int = 0):
        event = kwargs
        self.events.append(event)

        spell = WowSpell(**kwargs)
        spell.spec = self
        self.spells.append(spell)
