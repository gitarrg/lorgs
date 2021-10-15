"""All Playable Classes in the Game."""
from lorgs.data.classes.deathknight import *
from lorgs.data.classes.demonhunter import *
from lorgs.data.classes.druid import *
from lorgs.data.classes.hunter import *
from lorgs.data.classes.mage import *
from lorgs.data.classes.monk import *
from lorgs.data.classes.other import *
from lorgs.data.classes.paladin import *
from lorgs.data.classes.priest import *
from lorgs.data.classes.rogue import *
from lorgs.data.classes.shaman import *
from lorgs.data.classes.warlock import *
from lorgs.data.classes.warrior import *

# a few collections used to assign trinkets and consumables
ALL_SPECS = TANK.specs + HEAL.specs + MDPS.specs + RDPS.specs
INT_SPECS = HEAL.specs + [PRIEST_SHADOW, SHAMAN_ELEMENTAL, MAGE, WARLOCK, DRUID_BALANCE]
AGI_SPECS = [HUNTER, ROGUE, SHAMAN_ENHANCEMENT, MONK_WINDWALKER, DRUID_FERAL, DEMONHUNTER]
STR_SPECS = [WARRIOR, PALADIN_RETRIBUTION, DEATHKNIGHT]
