

import os
import json
import typing


ROOT = "./test/fixtures/"


def save_fixture(filename: str, content):

    file_path = os.path.join(ROOT, filename)
    with open(file_path, "w", encoding="utf-8") as json_file:
        return json.dump(
            content, json_file,
            indent=4,
        )


def load_fixture(filename: str):

    file_path = os.path.join(ROOT, filename)
    with open(file_path, "rb") as json_file:
        return json.load(json_file)


def wrap_data(data: typing.Any, *parents: str):
    """Wraps the `data` in a nested dict.
    
    Example:
        >>> wrap_data([1, 2, 3], "foo", "bar")
        {'foo': {'bar': [1, 2, 3]}}
    """
    parents = parents[::-1]
    for parent in parents:
        data = {parent: data}
    return data
