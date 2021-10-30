from lorgs import utils


################################################################################
# str_int_list
#
def test__str_int_list__basic_input():
    assert utils.str_int_list("8.5.4") == [8, 5, 4]


def test__str_int_list__empty_input():
    assert utils.str_int_list("") == []


################################################################################
# get_nested_value
#

def test__get_nested_value__empty_input():
    assert utils.get_nested_value({}, "attr", "name") == None


def test__get_nested_value__simple():
    data = {"attr": {"name": 5}}
    assert utils.get_nested_value(data, "attr", "name") == 5

def test__get_nested_value__simple_deep():
    data = {
        "some": {
            "deep": {
                "nested": {
                    "attr": {
                        "name": "Hello!"
                    }
                }
            }
        }
    }

    assert utils.get_nested_value(data, "some", "deep", "nested", "attr", "name") == "Hello!"


def test__get_nested_value__default():
    data = {"attr": {"name": 5}}
    assert utils.get_nested_value(data, "attr", "other", default=32) == 32
