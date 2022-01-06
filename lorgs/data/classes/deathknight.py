"""Define the Death Knight Class and all its Specs and Spells."""
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
DEATHKNIGHT = WowClass(id=6, name="Death Knight", color="#C41E3A")

################################################################################
# Specs
#
DEATHKNIGHT_BLOOD  = WowSpec(role=TANK, wow_class=DEATHKNIGHT, name="Blood")
DEATHKNIGHT_FROST  = WowSpec(role=MDPS, wow_class=DEATHKNIGHT, name="Frost")
DEATHKNIGHT_UNHOLY = WowSpec(role=MDPS, wow_class=DEATHKNIGHT, name="Unholy")

################################################################################
# Spells
#
DEATHKNIGHT.add_spell(         spell_id=312202, cooldown=60,  duration=14, color=COL_KYR,   name="Shackle the Unworthy",  icon="ability_bastion_deathknight.jpg",          show=False)
DEATHKNIGHT.add_spell(         spell_id=311648, cooldown=60,  duration=8,  color=COL_VENTR, name="Swarming Mist",         icon="ability_revendreth_deathknight.jpg")
DEATHKNIGHT.add_spell(         spell_id=315443, cooldown=120, duration=12, color=COL_NECRO, name="Abomination Limb",      icon="ability_maldraxxus_deathknight.jpg",       show=False)
DEATHKNIGHT.add_spell(         spell_id=51052,  cooldown=120, duration=10, color="#d58cff", name="Anti-Magic Zone",       icon="spell_deathknight_antimagiczone.jpg",      show=False, spell_type=SPELL_TYPE_RAID)
DEATHKNIGHT.add_spell(         spell_id=48707,  cooldown=60,  duration=5,  color="#8ced53", name="Anti-Magic Shell",      icon="spell_shadow_antimagicshell.jpg",          show=False)
DEATHKNIGHT.add_spell(         spell_id=48792,  cooldown=180, duration=8,  color="#53aaed", name="Icebound Fortitude",    icon="spell_deathknight_iceboundfortitude.jpg")
DEATHKNIGHT.add_spell(         spell_id=49039,  cooldown=120, duration=10, color="#999999", name="Lichborne",             icon="spell_shadow_raisedead.jpg")

DEATHKNIGHT_BLOOD.add_spell(   spell_id=49028,  cooldown=120, duration=8,  color="#ffbd24", name="Dancing Rune Weapon",   icon="inv_sword_07.jpg")
DEATHKNIGHT_BLOOD.add_spell(   spell_id=55233,  cooldown=90,  duration=10,                  name="Vampiric Blood",        icon="spell_shadow_lifedrain.jpg")
DEATHKNIGHT_BLOOD.add_spell(   spell_id=206931, cooldown=30,  duration=3,  color="#c43025", name="Blooddrinker",          icon="ability_animusdraw.jpg",                  show=False)
DEATHKNIGHT_BLOOD.add_spell(   spell_id=194679, cooldown=25,  duration=4,  color="#ff9169", name="Rune Tap",              icon="spell_deathknight_runetap.jpg",           show=False)

DEATHKNIGHT_UNHOLY.add_spell(  spell_id=42650,  cooldown=240, duration=30,                  name="Army of the Dead",      icon="spell_deathknight_armyofthedead.jpg",                 tags=[TAG_DYNAMIC_CD])
DEATHKNIGHT_UNHOLY.add_spell(  spell_id=275699, cooldown=45,  duration=15,                  name="Apocalypse",            icon="artifactability_unholydeathknight_deathsembrace.jpg", tags=[TAG_DYNAMIC_CD])
DEATHKNIGHT_UNHOLY.add_spell(  spell_id=63560,  cooldown=45,  duration=15,                  name="Dark Transformation",   icon="achievement_boss_festergutrotface.jpg",               tags=[TAG_DYNAMIC_CD])
DEATHKNIGHT_UNHOLY.add_spell(  spell_id=115989, cooldown=45,  duration=14, color="#58c437", name="Unholy Blight",         icon="spell_shadow_contagion.jpg")

DEATHKNIGHT_FROST.add_spell(   spell_id=51271,  cooldown=60,  duration=12,                  name="Pillar of Frost",       icon="ability_deathknight_pillaroffrost.jpg",    show=False)
DEATHKNIGHT_FROST.add_spell(   spell_id=46585,  cooldown=120, duration=60, color="#c7ba28", name="Raise Dead",            icon="inv_pet_ghoul.jpg",                        show=False)
DEATHKNIGHT_FROST.add_spell(   spell_id=47568,  cooldown=120, duration=20, color="#88e8f2", name="Empower Rune Weapon",   icon="inv_sword_62.jpg")
DEATHKNIGHT_FROST.add_spell(   spell_id=152279, cooldown=120, duration=30, color="#52abff", name="Breath of Sindragosa",  icon="spell_deathknight_breathofsindragosa.jpg")
DEATHKNIGHT_FROST.add_spell(   spell_id=279302, cooldown=180,                               name="Frostwyrm's Fury",      icon="achievement_boss_sindragosa.jpg")

# Additional Spells (not tracked)
RAISE_ALLY = WowSpell(spell_id=61999, name="Raise Ally", icon="spell_shadow_deadofnight.jpg")
