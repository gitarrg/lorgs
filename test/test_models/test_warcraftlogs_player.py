
import unittest
from lorgs.models import warcraftlogs_player
from lorgs.models.wow_spell import WowSpell

from lorgs.clients import wcl

MOCK_SPELLS = [
    WowSpell(spell_id=1),
    WowSpell(spell_id=2),
    WowSpell(spell_id=3)
]


class TestPlayer(unittest.TestCase):


    def setUp(self):
        self.player = warcraftlogs_player.Player()

    def test_get_cast_query__includes_player_name(self):
        self.player.name = "PlayerName"
        query = self.player.get_cast_query(MOCK_SPELLS)
        assert "source.name='PlayerName'" in query

    def test_get_buff_query__includes_player_name(self):
        self.player.name = "PlayerName"
        query = self.player.get_buff_query(MOCK_SPELLS)
        assert "target.name='PlayerName'" in query

    def test__set_source_id_from_events(self) -> None:
        events = [
            wcl.ReportEvent(type="something else", sourceID=2),
            wcl.ReportEvent(type="cast", sourceID=4),
            wcl.ReportEvent(type="cast", sourceID=8),
        ]

        self.player.source_id = -2
        self.player.set_source_id_from_events(events)
        assert self.player.source_id == 4
