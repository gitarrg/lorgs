import unittest
from unittest import mock

from lorgs.models.wow_spell import WowSpell
from lorgs.models import warcraftlogs_boss


class TestBoss(unittest.TestCase):

    def setUp(self):
        self.boss = warcraftlogs_boss.Boss()

        # setup an example boss
        self.example_boss = mock.MagicMock()
        self.example_boss.spells = [WowSpell(spell_id=101), WowSpell(spell_id=102)]
        self.example_boss.buffs = [WowSpell(spell_id=201), WowSpell(spell_id=202)]

    def test_get_raid_boss__valid(self):
        with mock.patch("lorgs.models.raid_boss.RaidBoss.get") as get_boss_mock:
            get_boss_mock.return_value = "something"
            assert self.boss.raid_boss == "something"

    def test_get_sub_query__no_raid_boss(self):

        with mock.patch("lorgs.models.raid_boss.RaidBoss.get") as get_boss_mock:
            get_boss_mock.return_value = None
            assert self.boss.get_sub_query() == ""

    def test_get_sub_query(self):

        with mock.patch("lorgs.models.raid_boss.RaidBoss.get") as get_boss_mock:
            get_boss_mock.return_value = self.example_boss

            query = self.boss.get_sub_query()

        expected = "("
        expected += "(type='cast' and ability.id in (101,102))" # casts
        expected += " or "
        expected += "(type in ('applybuff', 'removebuff') and ability.id in (201,202))" # buffs
        expected += ")"

        assert query == expected

