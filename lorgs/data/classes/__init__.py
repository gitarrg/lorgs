"""All Playable Classes in the Game."""
import typing
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
INT_SPECS: typing.List["WowSpec"] = HEAL.specs +  MAGE.specs + WARLOCK.specs + [PRIEST_SHADOW, SHAMAN_ELEMENTAL, DRUID_BALANCE]
AGI_SPECS: typing.List["WowSpec"] = HUNTER.specs + ROGUE.specs + [SHAMAN_ENHANCEMENT, MONK_BREWMASTER, MONK_WINDWALKER, DRUID_FERAL] + DEMONHUNTER.specs
STR_SPECS: typing.List["WowSpec"] = WARRIOR.specs + [PALADIN_PROTECTION, PALADIN_RETRIBUTION] + DEATHKNIGHT.specs
