import unittest

import arrow

from lorgs.models.warcraftlogs_report import Report


class TestReport(unittest.TestCase):

    def setUp(self) -> None:
        self.report = Report(report_id="REPORT_ID")

    def test__get_query(self):

        query = self.report.get_query()
        assert "REPORT_ID" in query

    def test__process_query_result__title(self):

        query_result = {"report": {"title": "new title"}}

        assert self.report.title != "new title"
        self.report.process_query_result(query_result=query_result)
        assert self.report.title == "new title"

    def test__process_query_result__start_time(self):

        query_result = {"report": {"startTime": 123456}}

        assert self.report.start_time == arrow.get(0)
        self.report.process_query_result(query_result=query_result)
        assert self.report.start_time == arrow.get(123456)

    def test__process_query_result__zone_id_valid(self):

        query_result = {"report": {"zone": {"id": 42}}}

        self.report.process_query_result(query_result=query_result)
        assert self.report.zone_id == 42

    def test__process_query_result__zone_id_invalid(self):

        query_result = {}

        self.report.process_query_result(query_result=query_result)
        assert self.report.zone_id == -1

    ############################################################################
    #
    # _process_master_data
    #

    def test__process_master_data__clears_data(self):
        self.report.players = {1: "old", 2: "players"}

        self.report.process_master_data({"some": "data"})
        assert self.report.players == {}

    ############################################################################
    #
    # add player
    #

    def test__add_player__create_player(self):

        actor_data = {
            "id": 32,
            "name": "PlayerName",
            "icon": "Shaman-Restoration",
            "type": "Player",
            "subType": "Shaman"
        }

        self.report.add_player(**actor_data)

        assert 32 in self.report.players
        player = self.report.players[32]
        assert player.source_id == 32
        assert player.name == "PlayerName"
        assert player.spec_slug == "shaman-restoration"
        assert player.class_slug == "shaman"

    def test__add_player__unknown_spec(self):

        actor_data = {
            "id": 5,
            "icon": "Hunter",
            "subType": "Hunter"
        }

        self.report.add_player(**actor_data)

        assert 5 in self.report.players
        player = self.report.players[5]
        assert player.spec_slug == ""
        assert player.class_slug == "hunter"

    ############################################################################
    #
    # process_report_fights
    #
    EXAMPLE_FIGHTS_DATA_1 = [
        {
            "code": 1,
            "encounterID": 2407,
            "fightPercentage": 70.99,
            "kill": False,
            "startTime": 406559,
            "endTime": 589257
        },
        {
            "code": 2,
            "encounterID": 2407,
            "fightPercentage": 66.14,
            "kill": False,
            "startTime": 681738,
            "endTime": 919600
        },
    ]

    def test__add_fight__skip_trash_fight(self):

        fight_data = {"encounterID": None}
        self.report.add_fight(**fight_data)

        assert not self.report.fights

    def test__add_fight__basic(self):

        fight_data = {
            "code": 10,
            "encounterID": 2407,
            "fightPercentage": 70.99,
            "kill": False,
            "startTime": 406559,
            "endTime": 589257
        }
        self.report.add_fight(**fight_data)

        assert self.report.fights
        fight = self.report.fights[10]

        assert fight.percent == 70.99
        assert fight.kill == False  # pylint: disable=singleton-comparison
        assert fight.start_time.timestamp() == 406.559
        assert fight.end_time.timestamp() == 589.257

