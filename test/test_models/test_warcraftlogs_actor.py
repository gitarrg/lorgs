
import unittest
from unittest import mock

from lorgs.clients import wcl
from lorgs.models import warcraftlogs_actor
from lorgs.models import wow_class
from lorgs.models import wow_role
from lorgs.models import wow_spec
from lorgs.models.warcraftlogs_cast import Cast
from lorgs.models.wow_spell import WowSpell

from test import helpers


# Test Classes
# todo: move somewhere else or mock away
MOCK_ROLE = wow_role.WowRole(id=4, name="Test")
MOCK_CLASS = wow_class.WowClass(id=4, name="Test")
MOCK_SPEC = wow_spec.WowSpec(name="TestSpec", wow_class=MOCK_CLASS, role=MOCK_ROLE)



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

        expected = "type in ('applybuff','removebuff') and ability.id in (101,102)"

        # run and test
        q = self.actor.get_buff_query(spells)
        assert q == expected

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
        casts_data = helpers.wrap_data(casts_events, "reportData", "report", "events", "data")
        query_data = wcl.Query(**casts_data)

        self.actor.source_id = 10
        self.actor.process_query_result(query_data)

        assert self.actor.casts != []
        assert len(self.actor.casts) == 3

        cast = self.actor.casts[2]
        assert cast.spell_id == 103
        assert cast.timestamp == 1010

    def test__process_casts__ignore_other_source_ids(self):
        """Make sure a cast from another ID is not added"""
        casts_events = [{"sourceID": 123}]
        casts_data = helpers.wrap_data(casts_events, "reportData", "report", "events", "data")
        query_data = wcl.Query(**casts_data)

        assert not self.actor.casts
        self.actor.source_id = 10
        self.actor.process_query_result(query_data)
        assert not self.actor.casts

    ############################################################################
    #

    def test__process_auras__calc_buff_duration(self):
        events = [
            Cast(spell_id=10, timestamp=100, event_type="applybuff"),
            Cast(spell_id=10, timestamp=250, event_type="removebuff"),
        ]

        result = self.actor.process_auras(events)

        assert len(result) == 1  # the removebuff event should be dropped
        event = result[0]
        assert event.timestamp == 100
        assert event.duration == 150

    def test__process_auras__multiple_applications(self):
        events = [
            Cast(spell_id=10, timestamp=110, event_type="applybuff"),
            Cast(spell_id=10, timestamp=120, event_type="applybuff"),
            Cast(spell_id=10, timestamp=130, event_type="applybuff"),
            Cast(spell_id=10, timestamp=250, event_type="removebuff"),
        ]

        result = self.actor.process_auras(events)

        assert len(result) == 1  # the removebuff event should be dropped
        event = result[0]
        assert event.timestamp == 110
        assert event.duration == 140

    def test__process_auras__multiple_buffs_same_spell(self):
        events = [
            Cast(spell_id=10, timestamp=100, event_type="applybuff"),
            Cast(spell_id=10, timestamp=150, event_type="removebuff"),
            Cast(spell_id=10, timestamp=200, event_type="applybuff"),
            Cast(spell_id=10, timestamp=260, event_type="removebuff"),
        ]

        result = self.actor.process_auras(events)

        assert len(result) == 2  # the removebuff event should be dropped
        eventA = result[0]
        assert eventA.timestamp == 100
        assert eventA.duration == 50

        eventB = result[1]
        assert eventB.timestamp == 200
        assert eventB.duration == 60

    def test__process_auras__multiple_buffs_diff_spell(self):
        events = [
            Cast(spell_id=10, timestamp=100, event_type="applybuff"),
            Cast(spell_id=20, timestamp=120, event_type="applybuff"),
            Cast(spell_id=10, timestamp=150, event_type="removebuff"),
            Cast(spell_id=20, timestamp=260, event_type="removebuff"),
        ]

        result = self.actor.process_auras(events)

        assert len(result) == 2  # the removebuff event should be dropped
        eventA = result[0]
        assert eventA.timestamp == 100
        assert eventA.duration == 50  # 100-150

        eventB = result[1]
        assert eventB.timestamp == 120
        assert eventB.duration == 140  # 120 - 260

    def test__process_auras__automatic_start(self) -> None:
        events = [
            # Aura fading 4sec into fight
            Cast(spell_id=10, timestamp=4000, event_type="removebuff"),
        ]

        # mock the spell to return 6sec as its default duration
        with mock.patch("lorgs.models.wow_spell.WowSpell.get") as mock_get_spell:
            mock_get_spell.return_value = mock.MagicMock()
            mock_get_spell.return_value.duration = 6

            # Run
            result = self.actor.process_auras(events)

        assert len(result) == 1  # still one everny
        event = result[0]
        assert event.timestamp == -2000
        assert event.event_type == "applybuff"

    def test__load_fixture_report_data_1(self) -> None:

        query_result = helpers.load_fixture("report_data_1.json")
        query_data = wcl.Query(**query_result)

        self.actor.source_id == 4
        self.actor.process_query_result(query_data)

        assert len(self.actor.casts) == 21
        assert self.actor.source_id == 4
