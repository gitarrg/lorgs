import sys
import pytest
from lorgs import utils


################################################################################
# str_int_list
#
def test__str_int_list__basic_input():
    assert utils.str_int_list("8.5.4") == [8, 5, 4]


def test__str_int_list__empty_input():
    assert utils.str_int_list("") == []


class TestGroupBy:
    def test__group_by__empty_input(self):
        items: list = []
        assert utils.group_by(*items, keyfunc=lambda x: "") == {}

    def test__group_by__1(self):

        items = ["foo", "bar", "a", "b", "c"]

        result = utils.group_by(*items, keyfunc=lambda x: len(x))
        assert result == {3: ["foo", "bar"], 1: ["a", "b", "c"]}


if __name__ == "__main__":
    pytest.main(sys.argv)
