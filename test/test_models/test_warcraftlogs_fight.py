import unittest
import pytest
import arrow
from unittest import mock


from lorgs.models import warcraftlogs_fight
from lorgs.models.raid_boss import RaidBoss
from lorgs.models.raid_zone import RaidZone


# pylint: disable=protected-access
# pylint: disable=attribute-defined-outside-init


def create_fake_player(role="", spec=""):
    player = mock.MagicMock()
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
        self.fight.duration = 3
        self.fight.boss_id = RAID_BOSS_ID

        self.fight.report = mock.MagicMock()
        self.fight.report.start_time = arrow.get(100.000)
        self.fight.report.report_id = "REPORT_ID"


    def test_start_time_rel(self):
        self.fight.report.start_time = arrow.get(100.000)
        self.fight.start_time = arrow.get(101.000)
        assert self.fight.start_time_rel == 1000

    def test_end_time_rel(self):
        self.fight.report.start_time = arrow.get(100.000)
        self.fight.start_time = arrow.get(101.000)
        self.fight.duration = 5  # in seconds
        assert self.fight.end_time_rel == 6000

    def test_table_query_args(self):
        result = self.fight.table_query_args
        assert result == "fightIDs: 5, startTime: 1000, endTime: 4000"

    #############################################
    # Get Query
    def test_get_player_query__no_players(self):
        self.fight.players = []
        query = self.fight.get_player_query()
        assert query == "players: table(fightIDs: 5, startTime: 1000, endTime: 4000, dataType: Summary)"

    def test_get_player_query__with_players(self):
        self.fight.players = ["A", "B"]   # just anything non zero
        query = self.fight.get_player_query()
        assert query == ""

    def test_get_player_casts_query__no_players(self):
        self.fight.players = []
        self.assertRaises(ValueError, self.fight.get_player_casts_query)

    def test_get_casts_query__skips_players_with_casts(self):

        player_A = create_fake_player()
        player_A.casts = []
        player_B = create_fake_player()
        player_B.casts = ["some", "values"]
        self.fight.players = [player_A, player_B]

        _ = self.fight.get_player_casts_query()

        assert player_A.get_sub_query.called
        assert not player_B.get_sub_query.called

    def test_get_boss_query__do_nothing_if_already_loaded(self):
        self.fight.boss = mock.MagicMock()
        self.fight.boss.casts = ["some", "casts"]
        assert self.fight.get_boss_query() == ""

    def test_get_boss_query__no_boss(self):
        self.fight.boss_id = 321 # some invalid valie
        assert self.fight.get_boss_query() == ""

    @mock.patch("lorgs.models.raid_boss.RaidBoss.get_sub_query")
    def test_get_boss_query___valid(self, raid_boss_get_sub_query_mock):

        raid_boss_get_sub_query_mock.return_value = "RaidBossQuery"

        assert not raid_boss_get_sub_query_mock.called
        query = self.fight.get_boss_query()
        assert raid_boss_get_sub_query_mock.called
        assert "RaidBossQuery" in query

    #############################################
    # Process Results: Boss
    def test_process_query_result_boss__no_input(self):

        self.fight.boss = mock.MagicMock()
        self.fight.boss.process_query_result = mock.MagicMock()
        self.fight.add_boss = mock.MagicMock()

        self.fight.process_boss(boss_data={})
        assert not self.fight.add_boss.called
        assert not self.fight.boss.process_query_result.called

    def test_process_boss__use_boss_if_exists(self):
        self.fight.boss = "something"
        self.fight.add_boss = mock.MagicMock()

        self.fight.process_boss(boss_data={})

        assert not self.fight.add_boss.called

    def test_process_boss__valid(self):

        boss_data = {"some": "data"}

        self.fight.boss = mock.MagicMock()
        self.fight.boss.process_query_result = mock.MagicMock()

        self.fight.process_boss(boss_data=boss_data)

        self.fight.boss.process_query_result.assert_called_once_with(boss_data)


class TestFight_ProcessPlayers(unittest.TestCase):


    def setUp(self):
        self.fight = warcraftlogs_fight.Fight()

        self.patch_get_spec = mock.patch("lorgs.models.wow_spec.WowSpec.get")
        # self.mock_get_spec.start()


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
        player_mock = mock.MagicMock()
        self.fight.add_player = mock.MagicMock(return_value=player_mock)

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

        with self.patch_get_spec as mock_get_spec:
            mock_get_spec.return_value = mock.MagicMock()
            mock_get_spec.return_value.full_name_slug = "fake_spec"

            self.fight.process_players(data)

            mock_get_spec.assert_called_with(name_slug_cap="TestSpec", wow_class__name_slug_cap="TestClass")
            assert self.fight.add_player.called
            assert player_mock.spec_slug == "fake_spec"
