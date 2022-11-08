import sys
import unittest
from unittest import mock

import pytest

from lorgs.models.warcraftlogs_actor import BaseActor
from lorgs.models import wow_class
from lorgs.models import wow_role
from lorgs.models import wow_spec
from lorgs.models.warcraftlogs_cast import Cast
from lorgs.models.wow_actor import WowActor
from lorgs.models.wow_spell import WowSpell

from test import helpers


# Test Classes
# todo: move somewhere else or mock away
MOCK_ROLE = wow_role.WowRole(id=4, name="Test")
MOCK_CLASS = wow_class.WowClass(id=4, name="Test")
MOCK_SPEC = wow_spec.WowSpec(name="TestSpec", wow_class=MOCK_CLASS, role=MOCK_ROLE)


class TestBaseActor(unittest.TestCase):
    @mock.patch.multiple(BaseActor, __abstractmethods__=set())
    def setUp(self):
        self.actor = BaseActor()

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
        # inputs
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
        # inputs
        spells = [WowSpell(spell_id=101), WowSpell(spell_id=102)]

        expected = "type in ('applybuff','removebuff') and ability.id in (101,102)"

        # run and test
        q = self.actor.get_buff_query(spells)
        assert q == expected

    ################################
    # get event query

    def test_get_event_query_empty(self):

        q = self.actor.get_events_query([])
        assert q == ""

    def test_get_event_query_events(self):
        # inputs
        events = [WowSpell(spell_id=101, event_type="damage")]

        # run and test
        result = self.actor.get_events_query(events)

        assert result == "(type='damage' and ability.id=101)"

    def test_get_event_query_events_include_until_evnets(self):
        # inputs
        events = [WowSpell(spell_id=101, until=WowSpell(spell_id=200))]

        # run and test
        result = self.actor.get_events_query(events)

        assert result == "(type='cast' and ability.id=101) or (type='cast' and ability.id=200)"

    ################################
    # process query result
    #
    def test__process_casts__simple(self):
        casts_events = [
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
                "abilityGameID": 103,
            },
        ]
        casts_data = helpers.wrap_data(casts_events, "report", "events", "data")

        self.actor.source_id = 10
        self.actor.process_query_result(**casts_data)

        assert self.actor.casts != []
        assert len(self.actor.casts) == 3

        cast = self.actor.casts[2]
        assert cast.spell_id == 103
        assert cast.timestamp == 1010

    def test__process_casts__ignore_other_source_ids(self):
        """Make sure a cast from another ID is not added"""
        casts_events = [{"sourceID": 123}]
        casts_data = helpers.wrap_data(casts_events, "report", "events", "data")

        assert not self.actor.casts
        self.actor.source_id = 10
        self.actor.process_query_result(**casts_data)
        assert not self.actor.casts


if __name__ == "__main__":
    pytest.main(sys.argv)
