"""Define the Evoker Class and all its Specs and Spells."""
# pylint: disable=line-too-long
# pylint: disable=bad-whitespace
# pylint: disable=wildcard-import
# pylint: disable=unused-wildcard-import

# IMPORT LOCAL LIBRARIES
from lorgs.data.constants import *
from lorgs.data.roles import *
from lorgs.models.wow_class import WowClass
from lorgs.models.wow_spec import WowSpec
from lorgs.models.wow_spell import WowSpell


################################################################################
# Class
#
EVOKER = WowClass(id=13, name="Evoker", color="#33937F")

################################################################################
# Specs
#
EVOKER_DEVASTATION = WowSpec(role=RDPS, wow_class=EVOKER, name="Devastation")
DRUID_PRESERVATION = WowSpec(role=HEAL, wow_class=EVOKER, name="Preservation")


################################################################################
# Spells
#
