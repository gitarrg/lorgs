
import unittest
from unittest import mock

from lorgs.models import warcraftlogs_actor, wow_class, wow_role, wow_spec
from lorgs.models.wow_spell import WowSpell

# pylint: disable=protected-access
# pylint: disable=attribute-defined-outside-init


# Test Classes
# todo: move somewhere else or mock away
MOCK_ROLE = wow_role.WowRole(id=4, name="Test")
MOCK_CLASS = wow_class.WowClass(id=4, name="Test")
MOCK_SPEC = wow_spec.WowSpec(name="TestSpec", wow_class=MOCK_CLASS, role=MOCK_ROLE)


class TestCast(unittest.TestCase):

    def test_get_end_time(self):
        cast = warcraftlogs_actor.Cast(timestamp=2000, duration=10)
        # start time + duration in MS
        assert cast.end_time == 2000 + 10000

    def test_set_end_time(self):
        cast = warcraftlogs_actor.Cast(timestamp=2000)
        cast.end_time = 10000

        assert cast.end_time == 10000
        assert cast.duration == 8  # in seconds


class TestBaseActor(unittest.TestCase):

    def setUp(self):
        self.actor = warcraftlogs_actor.BaseActor()
        return super().setUp()

    ################################
    # source id

    def test_has_source_id_true(self):
        self.actor.source_id = 5
        assert self.actor._has_source_id == True

    def test_has_source_id_false(self):
        assert self.actor._has_source_id == False
        self.actor.source_id = -1
        assert self.actor._has_source_id == False

    ################################
    # get_cast_query

    def test_get_cast_query_empty(self):
        q = self.actor.get_cast_query(spells=[])
        assert q == ""

    def test_get_cast_query_spells(self):
        #inputs
        spells = [WowSpell(spell_id=101), WowSpell(spell_id=102)]

        # run and test
        q = self.actor.get_cast_query(spells)
        assert q == "type='cast' and ability.id in (101,102)"

    ################################
    # get_buff_query

    def test_get_buff_query_empty(self):
        q = self.actor.get_buff_query(spells=[])
        assert q == ""

    def test_get_buff_query_spells(self):
        #inputs
        spells = [WowSpell(spell_id=101), WowSpell(spell_id=102)]

        expected = "type in ('applybuff', 'removebuff') and ability.id in (101,102)"

        # run and test
        q = self.actor.get_buff_query(spells)
        assert q == expected


class TestPlayer(unittest.TestCase):

    def setUp(self):
        self.player = warcraftlogs_actor.Player(
            spec_slug=MOCK_SPEC.full_name_slug
        )

    def test_spec(self):
        assert self.player.spec == MOCK_SPEC

    ################################
    # get_cast_query
    def test_get_cast_query_includes_name(self):
        # inputs
        spells = [WowSpell(spell_id=101)]
        self.player.name = "PlayerName"

        # run and test
        assert "source.name='PlayerName'" in self.player.get_cast_query(spells)

    def test_get_buff_query_includes_name(self):
        # inputs
        spells = [WowSpell(spell_id=101)]
        self.player.name = "PlayerName"

        # run and test
        assert "target.name='PlayerName'" in self.player.get_buff_query(spells)

    @mock.patch("lorgs.models.warcraftlogs_actor.BaseActor.get_cast_query")
    @mock.patch("lorgs.models.warcraftlogs_actor.BaseActor.get_buff_query")
    def get_sub_query(self, cast_query_mock: mock.MagicMock, buff_query_mock: mock.MagicMock):

        cast_query_mock.return_value = "CAST_QUERY"
        buff_query_mock.return_value = "BUFF_QUERY"


        query = self.player.get_sub_query()
        assert cast_query_mock.called_once()
        assert buff_query_mock.called_once()

        assert "CAST_QUERY" in query
        assert "BUFF_QUERY" in query
