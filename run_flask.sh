#!/usr/bin/env bash


# source ~/.envs/tvcSkyhooks/bin/activate
# pip install -r requirements.txt
# interwebs

export FLASK_ENV=development
export DEBUG=true

export PORT=5010
export FLASK_APP="lorgs/app:create_app()"


# Build SASS
# pysassc --style=compact lorgs/templates/scss/main.scss "lorgs/static/_generated/style.css"


# run flask
export PYTHONPATH=.  # adds current dir, so we can import
flask run --host=0.0.0.0 --port=$PORT
