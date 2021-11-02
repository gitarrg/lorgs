# IMPORT STANDARD LIBRARIES
import unittest
from unittest import mock


# IMPORT LOCAL LIBRARIES
from lorgs.models.warcraftlogs_ranking import SpecRanking
from ..helpers import load_fixture


class TestSpecRanking(unittest.TestCase):


    def setUp(self) -> None:
        self.spec_ranking = SpecRanking()

        self.boss_patch = mock.patch("lorgs.models.raid_boss.RaidBoss.get")
        self.boss_mock = self.boss_patch.start()
        self.boss_mock.return_value = mock.MagicMock(id=2048)


        self.spec_patch = mock.patch("lorgs.models.wow_spec.WowSpec.get")
        self.spec_mock = self.spec_patch.start()
        self.spec_mock.return_value = mock.MagicMock(**{
            "wow_class.name_slug_cap": "ClassName",
            "name_slug_cap": "SpecName",
            "role.metric": "metric",
        })

    def tearDown(self) -> None:
        self.boss_patch.stop()
        self.spec_patch.stop()


    def test__get_query(self):
        query = self.spec_ranking.get_query()

        assert 'className: "ClassName"' in query
        assert 'specName: "SpecName"' in query
        assert 'metric: metric' in query

    def test__process_query_result_one(self):

        data = {
            "worldData": {
                "encounter": {
                    "characterRankings": {
                        "rankings": [
                            {
                                "name": "PlayerName",
							    "amount": 123456,
							    "duration": 5432,
							    "startTime": 1634544096374,
							    "covenantID": 2,
							    "soulbindID": 9,
							    "report": {
								    "code": "REPORT_CODE",
								    "fightID": 5,
								    "startTime": 1634543354962
							    }
                            }
                        ]
                    }
                }
            }
        }
        self.spec_ranking.process_query_result(data)

        assert len(self.spec_ranking.reports) == 1

        report = self.spec_ranking.reports[0]
        assert report.report_id == "REPORT_CODE"

        fight = report.fights["5"]
        assert fight.fight_id == 5
        assert fight.duration == 5432

        player = fight.players["-1"]
        assert player.name == "PlayerName"
        assert player.total == 123456
        assert player.casts == []

    def test__process_query_result_fixture(self):

        data = load_fixture("spec_rankings_1.json")
        data = data.get("data")

        self.spec_ranking.process_query_result(data)

        assert len(self.spec_ranking.reports) == 10
