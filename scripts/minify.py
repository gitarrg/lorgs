#!/usr/bin/env python
"""Script to help minify our js files.

(in particular in cloud build)

this aims to replicate the behavior of
>>> python -m jsmin lorgs/static/timeline_modules/*.js >> lorgs/static/_generated/all_min.js

"""

import os
import glob
from jsmin import jsmin


BUILD_TAG = os.getenv("BUILD_TAG") or "BUILD_TAG"

PATH_OUT = f"lorgs/static/_generated/all_min_{BUILD_TAG}.js"
PATHS_IN = [
    "lorgs/static/*.js",
    "lorgs/static/timeline_modules/*.js"
]


def main():
    print("mimify main")
    print("> IN:", PATHS_IN)
    print("> OUT:", PATH_OUT)

    result = ""
    for path_in in PATHS_IN:
        for path in glob.glob(path_in):
            print("reading:", path)
            with open(path, "r") as f:
                result += jsmin(f.read())
                result += "\n"

    with open(PATH_OUT, "w") as fo:
        fo.write(result)

    print("done")

if __name__ == '__main__':
    main()
