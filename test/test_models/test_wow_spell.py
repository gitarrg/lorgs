import unittest

from lorgs.models.wow_spell import WowSpell



def test_spell_ids():

    spells = [WowSpell(spell_id=5), WowSpell(spell_id=3), WowSpell(spell_id=10)]

    result = WowSpell.spell_ids(spells)
    assert result == [3, 5, 10]


def test_spell_ids_str():

    spells = [WowSpell(spell_id=5), WowSpell(spell_id=3), WowSpell(spell_id=10)]

    result = WowSpell.spell_ids_str(spells)
    assert result == "3,5,10"


def test_is_item_spell__true():
    spell = WowSpell(spell_id=5, spell_type=WowSpell.TYPE_TRINKET)
    assert spell.is_item_spell() == True


def test_is_item_spell__false():
    spell = WowSpell(spell_id=5)
    assert spell.is_item_spell() == False


def test_is_healing_cooldown__item_spell():
    spell = WowSpell(spell_id=5, spell_type=WowSpell.TYPE_TRINKET)
    assert spell.is_healing_cooldown() == False


def test_is_healing_cooldown__personal():
    spell = WowSpell(spell_id=5, spell_type=WowSpell.TYPE_PERSONAL)
    assert spell.is_healing_cooldown() == False


def test_is_healing_cooldown__other():
    spell = WowSpell(spell_id=5)
    assert spell.is_healing_cooldown() == True

