#!/usr/bin/env bash


build_dir=_build




if [ -d "$build_dir/static" ]
then
    rm -r "$build_dir/static"
fi
cp -r wowtimeline/static $build_dir/static


source ~/.envs/wowtimeline/bin/activate
export PYTHONPATH=.  # adds current dir, so we can import from rcu_bot
python wowtimeline/main.py

