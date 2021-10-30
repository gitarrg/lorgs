# IMPORT STANDARD LIBRARIES
import unittest
from unittest import mock


# IMPORT LOCAL LIBRARIES
from lorgs.models.warcraftlogs_user_report import UserReport


class TestUserReport(unittest.TestCase):


    def setUp(self):
        self.user_report = UserReport()
        self.user_report.report = mock.MagicMock()

    def test__is_loaded__yes(self):
        self.user_report.report.fights = ["some", "values"]
        assert self.user_report.is_loaded

    def test__is_loaded__nope(self):
        self.user_report.report.fights = []
        assert not self.user_report.is_loaded

    def test__save__updates_timestamp(self):

        self.user_report.report.fights = []

        prev_value = self.user_report.updated

        with mock.patch("mongoengine.Document.save"):
            self.user_report.save()

        assert self.user_report.updated != prev_value
