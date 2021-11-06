
import unittest

from lorgs.models.warcraftlogs_cast import Cast


class TestCast(unittest.TestCase):
    def test_get_end_time(self):
        cast = Cast(timestamp=2000, duration=10000)
        # start time + duration in MS
        assert cast.end_time == 2000 + 10000

    def test_set_end_time(self):
        cast = Cast(timestamp=2000)
        cast.end_time = 10000

        assert cast.end_time == 10000
        assert cast.duration == 8000  # in seconds
