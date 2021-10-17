"""All the Constant Data for Lorrgs.

In here we create all our instances for the playable Roles, Classes, Specs and list their spells.

This could be stored in a Database instead..
but at the end of the day, this was the most straight forward way and the easiest to manage.

"""
# Roles and Classes
from lorgs.data.roles import *
from lorgs.data.classes import *

# Consumables, Gear and similar
from lorgs.data.covenants import *
from lorgs.data.potions import *
from lorgs.data.trinkets import *

# Raids
from lorgs.data.raids.t26_castle_nathria import *
from lorgs.data.raids.t28_sanctum_of_domination import *


CURRENT_ZONE = SANCTUM_OF_DOMINATION
