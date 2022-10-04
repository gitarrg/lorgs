"""RaidZone and Bosses for Patch 10.0 T31: Vault of the Incarnates, first raid tier of Dragonflight."""
# pylint: disable=line-too-long
# pylint: disable=C0326  # spaces

# IMPORT LOCAL LIBRARIES
from lorgs.models.raid_zone import RaidZone

################################################################################################################################################################
#
#   Tier: 30 Vault of the Incarnates
#
################################################################################################################################################################
RAID = RaidZone(id=31, name="Vault of the Incarnates")
VAULT_OF_THE_INCARNATES = RAID


################################################################################
# 01: Eranog
ERANOG = VAULT_OF_THE_INCARNATES.add_boss(id=2587, name="Eranog")


################################################################################
# 02: Terros
TERROS = VAULT_OF_THE_INCARNATES.add_boss(id=2639, name="Terros")


################################################################################
# 03: The Primal Council
PRIMAL_COUNCIL = VAULT_OF_THE_INCARNATES.add_boss(id=2590, name="The Primal Council")


################################################################################
# 04: Sennarth, The Cold Breath
SENNARTH = VAULT_OF_THE_INCARNATES.add_boss(id=2592, name="Sennarth, The Cold Breath", nick="Sennarth")


################################################################################
# 05: Dathea, Ascended
DATHEA = VAULT_OF_THE_INCARNATES.add_boss(id=2635, name="Dathea, Ascended", nick="Dathea")


################################################################################
# 06: Kurog Grimtotem
KUROG = VAULT_OF_THE_INCARNATES.add_boss(id=2605, name="Kurog Grimtotem", nick="Kurog")


################################################################################
# 07: Broodkeeper Diurna
DIURNA = VAULT_OF_THE_INCARNATES.add_boss(id=2614, name="Broodkeeper Diurna", nick="Diurna")


################################################################################
# 08: Raszageth the Storm-Eater
RASZAGETH = VAULT_OF_THE_INCARNATES.add_boss(id=2607, name="Raszageth the Storm-Eater", nick="Raszageth")

