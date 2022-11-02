import asyncio
from unittest import mock
import arrow
import json
import os
import pytest
import unittest
from lorgs.clients import wcl


from lorgs.models import warcraftlogs_fight
from lorgs.models.raid_boss import RaidBoss
from lorgs.models.raid_zone import RaidZone
from ..helpers import load_fixture

from lorgs import data


class TestFight(unittest.TestCase):


    def setUp(self):

        # Create a test Fight Instance
        self.fight = warcraftlogs_fight.Fight(
            fight_id = 5,
            start_time=arrow.get(101.000),
            duration=3000,
            boss_id=2000,
        )

        # a mock parent report
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


class TestFight_ProcessPlayers(unittest.TestCase):

    def setUp(self):
        self.fight = warcraftlogs_fight.Fight()

    ##########################################

    def test__empty(self):
        """Make sure no players get added."""
        self.fight.add_player = mock.MagicMock()
        self.fight.process_players(wcl.ReportSummary())
        assert not self.fight.add_player.called

    def test__valid_player(self):

        composition = [
            {
                "id": 1,
                "name": "Some Player",
                "type": "Druid",
                "specs": [{"spec": "Restoration"}]
            },
            {
                "id": 2,
                "name": "Other Player",
                "type": "DemonHunter",
                "specs": [{"spec": "Vengeance"}]
            },
        ]

        # print("summary_data", summary_data)
        # return
        # Run
        summary_data = wcl.ReportSummary(composition=composition)
        self.fight.process_players(summary_data)

        # Test
        assert len(self.fight.players) == 2
        assert list(self.fight.players.keys()) == ["1", "2"]

        player1 = self.fight.players["1"]
        assert player1.name == "Some Player"
        assert player1.spec.full_name_slug == "druid-restoration"
        player2 = self.fight.players["2"]
        assert player2.name == "Other Player"
        assert player2.spec.full_name_slug == "demonhunter-vengeance"


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
        fight = self.fight
        fight_data = load_fixture("fight_summary_1.json")
        fight_data = fight_data["data"]["reportData"]

        # run
        fight.process_query_result(**fight_data)

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
