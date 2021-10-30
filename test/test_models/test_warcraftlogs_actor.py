
import unittest
import random
from unittest import mock

import arrow

from lorgs.models import warcraftlogs_actor, warcraftlogs_fight, wow_class, wow_role, wow_spec
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

    ################################
    # process query result
    #
    def test__process_casts__simple(self):
        casts_data = {"data": [
            {
                "timestamp": 1001,
                "type": "cast",
                "sourceID": 10,
                "abilityGameID": 101,
            },
            {
                "timestamp": 1002,
                "type": "cast",
                "sourceID": 10,
                "abilityGameID": 102,
            },
            {
                "timestamp": 1010,
                "type": "cast",
                "sourceID": 10,
                "abilityGameID": 101,
            },
        ]}

        self.actor.source_id = 10
        self.actor.process_query_result(casts_data)

        assert self.actor.casts != []
        assert len(self.actor.casts) == 3

        cast = self.actor.casts[2]
        assert cast.spell_id == 101
        assert cast.timestamp == 1010

    def test__process_casts__ignore_other_source_ids(self):
        """Make sure a cast from another ID is not added"""
        casts_data = {"data": [
            {
                "sourceID": 123,
            }
        ]}

        assert not self.actor.casts
        self.actor.source_id = 10
        self.actor.process_query_result(casts_data)
        assert not self.actor.casts

    def test__process_casts__use_all_casts_if_actor_has_no_id(self):
        casts_data = {"data": [
            {"type": "cast", "sourceID": 1, "timestamp": 10, "abilityGameID": 0},
            {"type": "cast", "sourceID": 2, "timestamp": 20, "abilityGameID": 0},
            {"type": "cast", "sourceID": 3, "timestamp": 30, "abilityGameID": 0},
        ]}

        assert not self.actor.casts
        self.actor.source_id = -1
        self.actor.process_query_result(casts_data)
        assert len(self.actor.casts) == 3

    def test__process_query_result__calc_buff_duration(self):
        casts_data = {"data": [
            {"type": "applybuff",  "timestamp": 100, "abilityGameID": 10},
            {"type": "removebuff", "timestamp": 250, "abilityGameID": 10},
        ]}

        self.actor.process_query_result(casts_data)
        cast = self.actor.casts[0]
        assert cast.timestamp == 100
        assert cast.duration == 0.15

    def test__process_query_result__calc_buff_duration_when_applied_prepull(self):
        casts_data = {"data": [
            {"type": "removebuff", "timestamp": 4500, "abilityGameID": 10},
        ]}

        with mock.patch("lorgs.models.wow_spell.WowSpell.get") as mock_get_spell:
            mock_get_spell.return_value = mock.MagicMock()
            mock_get_spell.return_value.duration = 5  # 5 sec = 5000ms

            # Run
            self.actor.process_query_result(casts_data)

        # Test
        cast = self.actor.casts[0]
        assert cast.timestamp == -500


class TestPlayer(unittest.TestCase):

    def setUp(self):
        self.player = warcraftlogs_actor.Player(
            spec_slug=MOCK_SPEC.full_name_slug
        )
        self.spells = [WowSpell(spell_id=101)]

        self.cast_query_patch = mock.patch("lorgs.models.warcraftlogs_actor.BaseActor.get_cast_query")
        self.cast_query_mock = self.cast_query_patch.start()
        self.cast_query_mock.return_value = "CAST_QUERY"
        self.buff_query_patch = mock.patch("lorgs.models.warcraftlogs_actor.BaseActor.get_buff_query")
        self.buff_query_mock = self.buff_query_patch.start()
        self.buff_query_mock.return_value = "BUFF_QUERY"

    def tearDown(self):
        self.cast_query_patch.stop()
        self.buff_query_patch.stop()

    def test_spec(self):
        assert self.player.spec == MOCK_SPEC

    ################################
    # get_cast_query
    #

    def test_get_cast_query__includes_player_name(self):
        self.player.name = "PlayerName"

        query = self.player.get_cast_query()
        print("query", query)
        assert "source.name='PlayerName'" in query

    def test_get_buff_query__includes_player_name(self):
        self.player.name = "PlayerName"

        query = self.player.get_buff_query()
        assert "target.name='PlayerName'" in query

    def test_get_sub_query(self):

        query = self.player.get_sub_query()
        assert self.cast_query_mock.called_once()
        assert self.buff_query_mock.called_once()

        assert "CAST_QUERY" in query
        assert "BUFF_QUERY" in query
