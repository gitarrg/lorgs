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
XYMOX = SEPULCHER_OF_THE_FIRST_ONES.add_boss(id=2553, name="Artificer Xy'mox", nick="Xy'mox")
XYMOX.add_cast(spell_id=362801, duration=5.5, color="#e61919", name="Glyph of Relocation", icon="inv_axe_2h_broker_c_01.jpg") # Tank Grip
XYMOX.add_cast(spell_id=364465,               color="", name="Forerunner Rings",    icon="spell_broker_groundstate.jpg") # Rings
XYMOX.add_cast(spell_id=362721, duration=8.0, color="#ffc800", name="Dimensional Tear",    icon="spell_arcane_portalironforge.jpg") # Portals
XYMOX.add_buff(spell_id=367573,               color="#00ff00", name="Genesis Bulwark",     icon="inv_progenitor_runevessel.jpg") # Intermission
XYMOX.add_cast(spell_id=362885, duration=2.0, color="#00ffea", name="Stasis Trap",         icon="spell_broker_buff.jpg")


################################################################################
# 04: Dausegne, the Fallen Oracle
SEPULCHER_OF_THE_FIRST_ONES.add_boss(id=2540, name="Dausegne, the Fallen Oracle", nick="Dausegne")

################################################################################
# 05: Prototype Pantheon
SEPULCHER_OF_THE_FIRST_ONES.add_boss(id=2544, name="Prototype Pantheon")

################################################################################
# 06: Lihuvim, Principal Architect
LIHUVIM = SEPULCHER_OF_THE_FIRST_ONES.add_boss(id=2539, name="Lihuvim, Principal Architect", nick="Lihuvim")
LIHUVIM.add_cast(spell_id=364652, duration=1.9, color="#e61919", name="Protoform Cascade (Frontal)",      icon="spell_progenitor_debuff.jpg")
LIHUVIM.add_cast(spell_id=362601, duration=1.9, color="#00ffea", name="Unstable Mote (Mines)",            icon="spell_progenitor_orb.jpg")
LIHUVIM.add_cast(spell_id=363088, duration=3.0, color="#ffc800", name="Cosmic Shift (Knock)",             icon="spell_progenitor_areadenial.jpg")
LIHUVIM.add_cast(spell_id=363130, duration=4,   color="#00ff00", name="Synthesize (Intermission start)",  icon="spell_progenitor_beam.jpg")
LIHUVIM.add_cast(spell_id=361200, duration=20,  color="#00ff00", name="Recharge (intermission / mythic)", icon="spell_progenitor_buff.jpg")


################################################################################
# 07: Halondrus the Reclaimer
SEPULCHER_OF_THE_FIRST_ONES.add_boss(id=2529, name="Halondrus the Reclaimer", nick="Halondrus")

################################################################################
# 08: Anduin Wrynn
ANDUIN = SEPULCHER_OF_THE_FIRST_ONES.add_boss(id=2546, name="Anduin Wrynn", nick="Anduin")
ANDUIN.add_cast(spell_id=365030, duration=3.0, color="#d42020", name="Wicked Star",                       icon="spell_priest_divinestar_shadow2.jpg")
ANDUIN.add_cast(spell_id=365295, duration=2.0, color="#ebde34", name="Befouled Barrier",                  icon="inv_soulbarrier.jpg")
ANDUIN.add_cast(spell_id=362405, duration=35,  color="#34c6eb", name="Kingsmourne Hungers",               icon="ability_deathknight_hungeringruneblade.jpg")
ANDUIN.add_cast(spell_id=361989, duration=8.75,color="#a134eb", name="Blasphemy",                         icon="ability_priest_focusedwill.jpg")
ANDUIN.add_cast(spell_id=365958, duration=2.75,color="#a134eb", name="Hopelessness",                      icon="ability_priest_halo_shadow.jpg")
ANDUIN.add_buff(spell_id=362505,               color="#00ff00", name="Domination's Grasp (Intermission)", icon="spell_animamaw_buff.jpg")


################################################################################
# 09: Lords of Dread
SEPULCHER_OF_THE_FIRST_ONES.add_boss(id=2543, name="Lords of Dread")

################################################################################
# 10: Rygelon
SEPULCHER_OF_THE_FIRST_ONES.add_boss(id=2549, name="Rygelon")

################################################################################
# 11: The Jailer, Zovaal
SEPULCHER_OF_THE_FIRST_ONES.add_boss(id=2537, name="The Jailer, Zovaal", nick="Jailer")
