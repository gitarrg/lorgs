import sys
import pytest
from lorgs.models.wow_actor import WowActor
from lorgs.models.wow_spell import WowSpell


SPELL_10 = WowSpell(spell_id=10)
SPELL_20 = WowSpell(spell_id=20)


def test_all_spells() -> None:
    actor = WowActor()
    actor.add_spell(SPELL_10)

    assert actor.all_spells == [SPELL_10]


def test_all_spells_from_parent():

    parent = WowActor()
    actor = WowActor()
    actor.parents.append(parent)

    parent.add_spell(SPELL_10)
    assert actor.all_spells == [SPELL_10]


def test_all_spells_from_actor_and_parent():

    parent = WowActor()
    actor = WowActor()
    actor.parents.append(parent)

    parent.add_spell(SPELL_10)
    actor.add_spell(SPELL_20)

    assert actor.all_spells == [SPELL_10, SPELL_20]


if __name__ == "__main__":
    pytest.main(sys.argv)
