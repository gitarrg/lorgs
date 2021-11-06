

import os
import json


def load_fixture(file_name):

    file_path = os.path.join("./test/fixtures/", file_name)
    with open(file_path, "r") as json_file:
        return json.load(json_file)
