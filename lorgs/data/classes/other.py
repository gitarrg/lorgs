"""Special Utility Role/Class/Spec for things such as trinkets and potions."""
# pylint: disable=bad-whitespace
from lorgs.models.wow_class import WowClass
from lorgs.models.wow_role import WowRole
from lorgs.models.wow_spec import WowSpec


################################################################################
# Role
#
ITEM_ROLE     = WowRole(id=1001, code="item", name="Items")

################################################################################
# Class
#
OTHER         = WowClass(id=1001, name="Other", color="#cccccc")

################################################################################
# "Specs"
#
OTHER_POTION  = WowSpec(role=ITEM_ROLE, wow_class=OTHER, name="Potions")
OTHER_TRINKET = WowSpec(role=ITEM_ROLE, wow_class=OTHER, name="Trinkets")
OTHER_BUFFS = WowSpec(role=ITEM_ROLE, wow_class=OTHER, name="Buffs")
