

import os
import json


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

