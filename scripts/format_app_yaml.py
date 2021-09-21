#!/usr/bin/env python
"""Script to help pass variables to our app.yaml."""

import os
import sys
import random
import string

# set default build tag
os.environ.setdefault("BUILD_TAG", "BUILD_TAG")

# set random secret key
s = ''.join(random.choices(string.ascii_letters + string.digits, k=64))
os.environ.setdefault("SECRET_KEY", s)


FILE_IN = sys.argv[1]


with open(FILE_IN, "r") as f:
    content = f.read()
    content = content.format(**os.environ)
    print(content)
