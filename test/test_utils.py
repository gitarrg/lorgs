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


if __name__ == "__main__":
    pytest.main(sys.argv)
