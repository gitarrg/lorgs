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
SKOLEX = SEPULCHER_OF_THE_FIRST_ONES.add_boss(id=2542, name="Skolex, the Insatiable Ravener", nick="Skolex")
SKOLEX.add_cast(spell_id=359770, duration=7.0, color="#19d9e3", name="Ravening Burrow", icon="ability_argus_soulburst.jpg") # Phase Trigger
SKOLEX.add_cast(spell_id=360451, duration=6.5, color="#9919e3", name="Retch", icon="spell_nature_acid_01.jpg")              # Frontal
SKOLEX.add_cast(spell_id=359829, duration=2.5, color="#e3ad19", name="Dust Flail", icon="ability_butcher_whirl.jpg")        # Debuff Stacks
SKOLEX.add_cast(spell_id=359975, duration=2.5, color="", name="Riftmaw", icon="inv_netherportal.jpg", show=False)
SKOLEX.add_cast(spell_id=359979, duration=2.5, color="", name="Rend", icon="inv_sword_2h_artifactsoulrend_d_06.jpg", show=False)
SKOLEX.add_cast(spell_id=364622, duration=0.0, color="", name="Final Consumption", icon="spell_shadow_unholyfrenzy.jpg")

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
