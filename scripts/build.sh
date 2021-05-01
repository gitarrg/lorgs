#!/usr/bin/env bash


build_dir=_build


if [ -d "$build_dir/static" ]
then
    rm -r "$build_dir/static"
fi
cp -r lorgs/static $build_dir/static


# Build SASS
# pysassc --style=compact lorgs/templates/scss/main.scss "$build_dir/static/style.css"

# Watchdog
# pysass --style=compact lorgs/templates/scss/main.scss "lorgs/static/_generated/style.css" -I lorgs/templates/scss --watch 


# source ~/.envs/lorgs/bin/activate
# export PYTHONPATH=.  # adds current dir, so we can import from rcu_bot
# python lorgs/main.py

