#!/usr/bin/env python
"""Models for Raids and RaidBosses."""

# IMPORT LOCAL LIBRARIES
from lorgs.models.encounters import RaidZone


CASTLE_NATHRIA = RaidZone(id=26, name="Castle Nathria")
CASTLE_NATHRIA.add_boss(id=2398, name="Shriekwing")
CASTLE_NATHRIA.add_boss(id=2418, name="Huntsman Altimor")
CASTLE_NATHRIA.add_boss(id=2383, name="Hungering Destroyer")
CASTLE_NATHRIA.add_boss(id=2402, name="Sun King's Salvation")
CASTLE_NATHRIA.add_boss(id=2405, name="Artificer Xy'mox")
CASTLE_NATHRIA.add_boss(id=2406, name="Lady Inerva Darkvein")
CASTLE_NATHRIA.add_boss(id=2412, name="The Council of Blood")
CASTLE_NATHRIA.add_boss(id=2399, name="Sludgefist")
CASTLE_NATHRIA.add_boss(id=2417, name="Stone Legion Generals")
CASTLE_NATHRIA.add_boss(id=2407, name="Sire Denathrius")


CASTLE_NATHRIA_BOSSES = CASTLE_NATHRIA.bosses
