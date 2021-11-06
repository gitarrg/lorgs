import asyncio
from unittest import mock
import arrow
import json
import os
import pytest
import unittest


from lorgs.models import warcraftlogs_fight
from lorgs.models.raid_boss import RaidBoss
from lorgs.models.raid_zone import RaidZone
from ..helpers import load_fixture


# pylint: disable=protected-access
# pylint: disable=attribute-defined-outside-init


def create_fake_player(role="", spec="", **kwargs):
    player = mock.MagicMock(**kwargs)
    player.spec.role.code = role
    player.spec.full_name_slug = spec

    player.get_sub_query = mock.MagicMock(return_value="player.get_sub_query")
    player.get_cast_query = mock.MagicMock(return_value="player.get_cast_query")
    player.get_buff_query = mock.MagicMock(return_value="player.get_buff_query")
    return player


RAID_BOSS_ID = 2000


@pytest.fixture(autouse=True)
def test_raid_boss():
    # create a raid boss instance, so we have something to test againt
    zone = RaidZone(id=1, name="TestZone")
    boss = RaidBoss(id=RAID_BOSS_ID, zone=zone, name="TestBoss")
    return boss





class TestGetComposition(unittest.TestCase):

    def setUp(self):
        self.players = [
            create_fake_player(role="tank", spec="specA"),
            create_fake_player(role="tank", spec="specB"),
            create_fake_player(role="heal", spec="specA"),
            create_fake_player(role="mdps", spec="specC"),
            create_fake_player(role="rdps", spec="specB"),
        ]


    def test_empty(self):

        result = warcraftlogs_fight.get_composition(players=[])
        expected = {"roles": {}, "specs": {}, "classes": {}}

        assert result == expected

    def test_roles(self):
        result = warcraftlogs_fight.get_composition(players=self.players)
        result_roles = result["roles"]
        assert result_roles["tank"] == 2
        assert result_roles["heal"] == 1
        assert result_roles["mdps"] == 1
        assert result_roles["rdps"] == 1

    def test_specs(self):
        result = warcraftlogs_fight.get_composition(players=self.players)
        result_specs = result["specs"]
        assert result_specs["specA"] == 2
        assert result_specs["specB"] == 2
        assert result_specs["specC"] == 1


class TestFight(unittest.TestCase):


    def setUp(self):
        self.fight = warcraftlogs_fight.Fight()
        self.fight.fight_id = 5
        self.fight.start_time = arrow.get(101.000)
        self.fight.duration = 3000
        self.fight.boss_id = RAID_BOSS_ID

        self.fight.report = mock.MagicMock()
        self.fight.report.start_time = arrow.get(100.000)
        self.fight.report.report_id = "REPORT_ID"

    def test_start_time_rel(self):
        self.fight.report.start_time = arrow.get(100.000)
        self.fight.start_time = arrow.get(121.000)
        assert self.fight.start_time_rel == 21000

    def test_end_time_rel(self):
        self.fight.report.start_time = arrow.get(100.000)
        self.fight.start_time = arrow.get(120.000)
        self.fight.duration = 600 * 1000
        assert self.fight.end_time_rel == 620 * 1000

    def test_table_query_args(self):
        result = self.fight.table_query_args
        assert result == "fightIDs: 5, startTime: 1000, endTime: 4000"

    #############################################
    # Get Query: Summary
    #

    def test_get_summary_query__no_players(self):
        self.fight.players = []
        query = self.fight.get_summary_query()
        expected = "table(fightIDs: 5, startTime: 1000, endTime: 4000, dataType: Summary)"
        assert expected in query

    def test_get_summary_query__with_players(self):
        self.fight.players = ["A", "B"]   # just anything non zero
        query = self.fight.get_summary_query()
        assert query == ""


class TestFight_ProcessPlayers(unittest.TestCase):

    def setUp(self):
        self.fight = warcraftlogs_fight.Fight()

    ##########################################

    def test__empty(self):
        """Make sure no players get added."""
        self.fight.add_player = mock.MagicMock()
        self.fight.process_players({})
        assert not self.fight.add_player.called

    def test__invalid_class(self):
        self.fight.add_player = mock.MagicMock()

        data = {
            "composition": [
                {
                    "name": "Some Player",
                    "type": "InvalidClassName",  # <--
                }
            ]
        }
        self.fight.process_players(data)
        assert not self.fight.add_player.called

    def test__valid_player(self):
        data = {
            "composition": [
                {
                    "name": "Some Player",
                    "type": "TestClass",  # <--
                    "specs": [{
                        "spec": "TestSpec",
                    }]
                }
            ]
        }

        with mock.patch("lorgs.models.wow_spec.WowSpec.get") as mock_get_spec:
            mock_get_spec.return_value = mock.MagicMock()
            mock_get_spec.return_value.full_name_slug = "fake_spec"

            self.fight.process_players(data)

            mock_get_spec.assert_called_with(full_name_slug="fake_spec")

    def test__example_fixture1(self):
        """Test an example Response.

        load via:
        >>> query {
        >>>     reportData {
        >>>         report(code: "Jx1cWpb8nFLhBfPa") {
        >>>             summary: table(fightIDs: 19, startTime: 10881328, endTime: 11609926, dataType: Summary)
        >>>         }
        >>>     }
        >>> }

        """
        # load class/specs
        from lorgs import data  # pylint: disable=unused-import

        fight = self.fight

        fight_data = load_fixture("fight_summary_1.json")
        fight_data = fight_data.get("data")
        fight.process_overview(fight_data)

        assert len(fight.players) == 20
        assert fight.duration == 728598

        # check if the comp was loaded
        comp = fight.composition
        assert comp["roles"]["tank"] == 2
        assert comp["roles"]["heal"] == 4
        assert comp["specs"]["hunter-marksmanship"] == 2
        assert comp["specs"]["monk-windwalker"] == 1
        assert comp["classes"]["warlock"] == 2

        # test a player from the report
        player_arrg = fight.get_player(source_id=17)
        assert player_arrg.name == "Arrg"  # thats me!!
        assert player_arrg.spec_slug == "druid-restoration"
        assert player_arrg.total == 10761
