import sys
import unittest

import pytest
from lorgs.models import warcraftlogs_player

from lorgs.clients import wcl


class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.player = warcraftlogs_player.Player()

    def test__set_source_id_from_events(self) -> None:
        events = [
            wcl.ReportEvent(type="something else", sourceID=2),
            wcl.ReportEvent(type="cast", sourceID=4),
            wcl.ReportEvent(type="cast", sourceID=8),
        ]

        self.player.source_id = -2
        self.player.set_source_id_from_events(events)
        assert self.player.source_id == 4


if __name__ == "__main__":
    pytest.main(sys.argv)
