#!/usr/bin/env bash


# get current path
full_path=$(realpath $0)
dir_path=$(dirname $full_path)


# python $dir_path/delete_all.py
export PYTHONPATH=.  # adds current dir, so we can import
python $dir_path/init_tables.py
python $dir_path/init_encounters.py
python $dir_path/init_specs.py
python $dir_path/init_spells.py
python $dir_path/load_spell_icons.py

