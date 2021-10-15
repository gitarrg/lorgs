from lorgs.models.wow_role import WowRole

################################################################################
# ROLES
#
TANK = WowRole(id=1, code="tank", name="Tank")
HEAL = WowRole(id=2, code="heal", name="Healer")
MDPS = WowRole(id=3, code="mdps", name="Melee")
RDPS = WowRole(id=4, code="rdps", name="Range")
ALL_ROLES = [TANK, HEAL, MDPS, RDPS]
