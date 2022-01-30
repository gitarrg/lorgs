"""RaidZone and Bosses for Patch 9.2 T29: Sepulcher of the First Ones, third tier of Shadowlands."""
# pylint: disable=line-too-long
# pylint: disable=C0326  # spaces

# IMPORT LOCAL LIBRARIES
from lorgs.models.raid_zone import RaidZone


################################################################################################################################################################
#
#   Tier: 29 Sepulcher of the First Ones
#
################################################################################################################################################################
SEPULCHER_OF_THE_FIRST_ONES = RaidZone(id=29, name="Sepulcher of the First Ones")

################################################################################
# 01: Vigilant Guardian
SEPULCHER_OF_THE_FIRST_ONES.add_boss(id=2512, name="Vigilant Guardian")

################################################################################
# 02: Skolex, the Insatiable Ravener
SEPULCHER_OF_THE_FIRST_ONES.add_boss(id=2542, name="Skolex, the Insatiable Ravener", nick="Skolex")

################################################################################
# 03: Artificer Xy'mox
SEPULCHER_OF_THE_FIRST_ONES.add_boss(id=2553, name="Artificer Xy'mox", nick="Xy'mox")

################################################################################
# 04: Dausegne, the Fallen Oracle
SEPULCHER_OF_THE_FIRST_ONES.add_boss(id=2540, name="Dausegne, the Fallen Oracle", nick="Dausegne")

################################################################################
# 05: Prototype Pantheon
SEPULCHER_OF_THE_FIRST_ONES.add_boss(id=2544, name="Prototype Pantheon")

################################################################################
# 06: Lihuvim, Principal Architect
SEPULCHER_OF_THE_FIRST_ONES.add_boss(id=2539, name="Lihuvim, Principal Architect", nick="Lihuvim")

################################################################################
# 07: Halondrus the Reclaimer
SEPULCHER_OF_THE_FIRST_ONES.add_boss(id=2529, name="Halondrus the Reclaimer", nick="Halondrus")

################################################################################
# 08: Anduin Wrynn
SEPULCHER_OF_THE_FIRST_ONES.add_boss(id=2546, name="Anduin Wrynn", nick="Anduin")

################################################################################
# 09: Lords of Dread
SEPULCHER_OF_THE_FIRST_ONES.add_boss(id=2543, name="Lords of Dread")

################################################################################
# 10: Rygelon
SEPULCHER_OF_THE_FIRST_ONES.add_boss(id=2549, name="Rygelon")

################################################################################
# 11: The Jailer, Zovaal
SEPULCHER_OF_THE_FIRST_ONES.add_boss(id=2537, name="The Jailer, Zovaal", nick="Jailer")
