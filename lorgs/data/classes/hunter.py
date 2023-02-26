"""Define the Hunter Class and all its Specs and Spells."""
# pylint: disable=line-too-long
# pylint: disable=bad-whitespace
# pylint: disable=wildcard-import
# pylint: disable=unused-wildcard-import
# fmt: off

# IMPORT LOCAL LIBRARIES
from lorgs.data.constants import *
from lorgs.data.roles import *
from lorgs.models.wow_class import WowClass
from lorgs.models.wow_spec import WowSpec


################################################################################
# Class
#
HUNTER = WowClass(id=3, name="Hunter", color="#AAD372")

################################################################################
# Specs
#
HUNTER_BEASTMASTERY   = WowSpec(role=RDPS, wow_class=HUNTER,       name="Beast Mastery")
HUNTER_MARKSMANSHIP   = WowSpec(role=RDPS, wow_class=HUNTER,       name="Marksmanship")
HUNTER_SURVIVAL       = WowSpec(role=MDPS, wow_class=HUNTER,       name="Survival")

################################################################################
# Spells
#
HUNTER.add_spell(              spell_id=328231, cooldown=120, duration=15, color=COL_NF,    name="Wild Spirits",        icon="ability_ardenweald_hunter.jpg")
HUNTER.add_spell(              spell_id=308491, cooldown=60,  duration=10, color=COL_KYR,   name="Resonating Arrow",    icon="ability_bastion_hunter.jpg")
HUNTER.add_spell(              spell_id=375891, cooldown=45,  duration=10, color=COL_NECRO, name="Death Chakram",    icon="ability_maldraxxus_hunter.jpg")


HUNTER.add_spell(              spell_id=109304, cooldown=120,                               name="Exhilaration",        icon="ability_hunter_onewithnature.jpg", show=False)
HUNTER.add_buff(               spell_id=186265, cooldown=120,                               name="Aspect of the Turtle",icon="ability_hunter_pet_turtle.jpg", show=False)
HUNTER.add_spell(              spell_id=264735, cooldown=180, duration=6,                   name="Survival of the Fittest", icon="spell_nature_spiritarmor.jpg", show=False, variations=[281195])
HUNTER.add_buff(               spell_id=339461, cooldown=30,                                name="Resilience of the Hunter",icon="ability_rogue_feigndeath.jpg", show=False) # Feint Death Conduit


HUNTER_BEASTMASTERY.add_spell( spell_id=193530, cooldown=180, duration=20,                  name="Aspect of the Wild",  icon="spell_nature_protectionformnature.jpg")
HUNTER_BEASTMASTERY.add_spell( spell_id=19574,  cooldown=30,  duration=15, color="#e6960f", name="Bestial Wrath",       icon="ability_druid_ferociousbite.jpg",        show=False)

HUNTER_MARKSMANSHIP.add_spell( spell_id=288613, cooldown=120, duration=15,                  name="Trueshot",            icon="ability_trueshot.jpg")
HUNTER_MARKSMANSHIP.add_spell( spell_id=260243, cooldown=45,  duration=6, color="#bf8686",  name="Volley",              icon="ability_hunter_rapidkilling.jpg",          show=False)

HUNTER_SURVIVAL.add_spell(     spell_id=360952, cooldown=120, duration=20,                  name="Coordinated Assault", icon="inv_coordinatedassault.jpg")
HUNTER_SURVIVAL.add_spell(     spell_id=186289, cooldown=90,  duration=15,                  name="Aspect of the Eagle", icon="spell_hunter_aspectoftheironhawk.jpg")
HUNTER_SURVIVAL.add_spell(     spell_id=360966, cooldown=90,  duration=12, color="#3aa65e", name="Spearhead",           icon="ability_hunter_spearhead.jpg")
