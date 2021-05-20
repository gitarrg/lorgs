#!/usr/bin/env python
"""Models for Raids and RaidBosses."""
# IMPORT STANDARD LIBRARIES

# pylint: disable=line-too-long
# pylint: disable=C0326  # spaces

# IMPORT LOCAL LIBRARIES
from lorgs.models.specs import WowClass
from lorgs.models.specs import WowRole
from lorgs.models.specs import WowSpec
from lorgs.models.specs import WowSpell

################################################################################
#
#   ROLES
#
################################################################################
TANK = WowRole(code="tank", name="Tank")
HEAL = WowRole(code="heal", name="Healer")
MDPS = WowRole(code="mdps", name="Melee")
RDPS = WowRole(code="rdps", name="Range")
ROLES = [TANK, HEAL, MDPS, RDPS]

################################################################################
#
#   CLASSES
#
WARRIOR      = WowClass(id=1,  name="Warrior",       color="#C69B6D")
PALADIN      = WowClass(id=2,  name="Paladin",       color="#F48CBA")
HUNTER       = WowClass(id=3,  name="Hunter",        color="#AAD372")
ROGUE        = WowClass(id=4,  name="Rogue",         color="#FFF468")
PRIEST       = WowClass(id=5,  name="Priest",        color="#FFFFFF")
DEATHKNIGHT  = WowClass(id=6,  name="Death Knight",  color="#C41E3A")
SHAMAN       = WowClass(id=7,  name="Shaman",        color="#0070DD")
MAGE         = WowClass(id=8,  name="Mage",          color="#3FC7EB")
WARLOCK      = WowClass(id=9,  name="Warlock",       color="#8788EE")
MONK         = WowClass(id=10, name="Monk",          color="#00FF98")
DRUID        = WowClass(id=11, name="Druid",         color="#FF7C0A")
DEMONHUNTER  = WowClass(id=12, name="Demon Hunter",  color="#A330C9")

CLASSES = list(WowClass.all)


################################################################################
#
#   SPECS
#
################################################################################

WARRIOR_ARMS          = WowSpec(role=MDPS, wow_class=WARRIOR,      name="Arms")
WARRIOR_FURY          = WowSpec(role=MDPS, wow_class=WARRIOR,      name="Fury")
WARRIOR_PROT          = WowSpec(role=TANK, wow_class=WARRIOR,      name="Protection",    short_name="Prot")
PALADIN_HOLY          = WowSpec(role=HEAL, wow_class=PALADIN,      name="Holy")
PALADIN_PROTECTION    = WowSpec(role=TANK, wow_class=PALADIN,      name="Protection",    short_name="Prot")
PALADIN_RETRIBUTION   = WowSpec(role=MDPS, wow_class=PALADIN,      name="Retribution",   short_name="Ret")
HUNTER_BEASTMASTERY   = WowSpec(role=RDPS, wow_class=HUNTER,       name="Beast Mastery")
HUNTER_MARKSMANSHIP   = WowSpec(role=RDPS, wow_class=HUNTER,       name="Marksmanship")
HUNTER_SURVIVAL       = WowSpec(role=MDPS, wow_class=HUNTER,       name="Survival")
ROGUE_ASSASSINATION   = WowSpec(role=MDPS, wow_class=ROGUE,        name="Assassination", short_name="Assa")
ROGUE_OUTLAW          = WowSpec(role=MDPS, wow_class=ROGUE,        name="Outlaw")
ROGUE_SUBTLETY        = WowSpec(role=MDPS, wow_class=ROGUE,        name="Subtlety")
PRIEST_DISCIPLINE     = WowSpec(role=HEAL, wow_class=PRIEST,       name="Discipline",    short_name="Disc")
PRIEST_HOLY           = WowSpec(role=HEAL, wow_class=PRIEST,       name="Holy")
PRIEST_SHADOW         = WowSpec(role=RDPS, wow_class=PRIEST,       name="Shadow")
DEATHKNIGHT_BLOOD     = WowSpec(role=TANK, wow_class=DEATHKNIGHT,  name="Blood")
DEATHKNIGHT_FROST     = WowSpec(role=MDPS, wow_class=DEATHKNIGHT,  name="Frost")
DEATHKNIGHT_UNHOLY    = WowSpec(role=MDPS, wow_class=DEATHKNIGHT,  name="Unholy")
SHAMAN_ELEMENTAL      = WowSpec(role=RDPS, wow_class=SHAMAN,       name="Elemental")
SHAMAN_ENHANCEMENT    = WowSpec(role=MDPS, wow_class=SHAMAN,       name="Enhancement")
SHAMAN_RESTORATION    = WowSpec(role=HEAL, wow_class=SHAMAN,       name="Restoration",   short_name="Resto")
MAGE_ARCANE           = WowSpec(role=RDPS, wow_class=MAGE,         name="Arcane")
MAGE_FIRE             = WowSpec(role=RDPS, wow_class=MAGE,         name="Fire")
MAGE_FROST            = WowSpec(role=RDPS, wow_class=MAGE,         name="Frost")
WARLOCK_AFFLICTION    = WowSpec(role=RDPS, wow_class=WARLOCK,      name="Affliction",    short_name="Aff")
WARLOCK_DEMONOLOGY    = WowSpec(role=RDPS, wow_class=WARLOCK,      name="Demonology",    short_name="Demo")
WARLOCK_DESTRUCTION   = WowSpec(role=RDPS, wow_class=WARLOCK,      name="Destruction",   short_name="Destro")
MONK_BREWMASTER       = WowSpec(role=TANK, wow_class=MONK,         name="Brewmaster")
MONK_MISTWEAVER       = WowSpec(role=HEAL, wow_class=MONK,         name="Mistweaver")
MONK_WINDWALKER       = WowSpec(role=MDPS, wow_class=MONK,         name="Windwalker")
DRUID_BALANCE         = WowSpec(role=RDPS, wow_class=DRUID,        name="Balance")
DRUID_FERAL           = WowSpec(role=MDPS, wow_class=DRUID,        name="Feral")
DRUID_GUARDIAN        = WowSpec(role=TANK, wow_class=DRUID,        name="Guardian")
DRUID_RESTORATION     = WowSpec(role=HEAL, wow_class=DRUID,        name="Restoration",   short_name="Resto")
DEMONHUNTER_HAVOC     = WowSpec(role=MDPS, wow_class=DEMONHUNTER,  name="Havoc")
DEMONHUNTER_VENGEANCE = WowSpec(role=TANK, wow_class=DEMONHUNTER,  name="Vengeance")

SPECS = list(WowSpec.all)

for spec in WowSpec.all:
    spec.role.specs.append(spec)

# sorry guys...
WARRIOR_PROT.supported = False
PALADIN_PROTECTION.supported = False
DEATHKNIGHT_BLOOD.supported = False
MONK_BREWMASTER.supported = False
DRUID_GUARDIAN.supported = False
DEMONHUNTER_VENGEANCE.supported = False

# mdps
WARRIOR_ARMS.supported = False
HUNTER_SURVIVAL.supported = False
ROGUE_ASSASSINATION.supported = False
ROGUE_SUBTLETY.supported = False
ROGUE_OUTLAW.supported = False
DEATHKNIGHT_FROST.supported = False
DRUID_FERAL.supported = False

# rdps
PRIEST_SHADOW.supported = False
MAGE_ARCANE.supported = False
MAGE_FROST.supported = False

SUPPORTED_SPECS = [spec for spec in SPECS if spec.supported]


################################################################################
#
#   OTHER
# its a bit of a hack.. but works for now
# all ids start at 1000 here, to help separate them later.
#
################################################################################

ROLE_ITEM     = WowRole(code="item", name="Items")
OTHER         = WowClass(id=1001, name="Other", color="#cccccc")
OTHER_POTION  = WowSpec(role=ROLE_ITEM, wow_class=OTHER, name="Potions")
OTHER_TRINKET = WowSpec(role=ROLE_ITEM, wow_class=OTHER, name="Trinkets")

################################################################################
#
#   CONSTANTS
#
################################################################################

# Some Colors
COL_NF    = "#8d5ca1"
COL_VENTR = "FireBrick"
COL_KYR   = "LightSkyBlue"
COL_NECRO = "MediumSeaGreen"
COL_MANA  = "#5397ed"


################################################################################
#
#       SPELLS: CLASSES / SPECS
#
################################################################################

#################################################################################################################################################################################################
#   Warrior
WARRIOR.add_spell(            spell_id=325886, cooldown=90,  duration=12, color=COL_NF,     name="Ancient Aftershock",              icon="ability_ardenweald_warrior.jpg")
WARRIOR.add_spell(            spell_id=97462,  cooldown=180, duration=10,                   name="Rallying Cry",                    icon="ability_warrior_rallyingcry.jpg",           show=False)
WARRIOR_FURY.add_spell(       spell_id=1719,   cooldown=60,  duration=10,                   name="Recklessness",                    icon="warrior_talent_icon_innerrage.jpg")
WARRIOR_FURY.add_spell(       spell_id=46924,  cooldown=60,  duration=4,                    name="Bladestorm",                      icon="ability_warrior_bladestorm.jpg")
#################################################################################################################################################################################################
#   Paladin
PALADIN.add_spell(             spell_id=304971, cooldown=60,               color=COL_KYR,   name="Divine Toll",                     icon="ability_bastion_paladin.jpg",               show=False)
PALADIN.add_spell(             spell_id=316958, cooldown=240, duration=30, color=COL_VENTR, name="Ashen Hallow",                    icon="ability_revendreth_paladin.jpg")
PALADIN.add_spell(             spell_id=31884,  cooldown=120, duration=20, color="#ffc107", name="Avenging Wrath",                  icon="spell_holy_avenginewrath.jpg")
PALADIN_HOLY.add_spell(        spell_id=31821,  cooldown=180, duration=8,  color="#dc65f5", name="Aura Mastery",                    icon="spell_holy_auramastery.jpg")
#################################################################################################################################################################################################
# Hunter
HUNTER.add_spell(              spell_id=328231, cooldown=120, duration=15, color=COL_NF,    name="Wild Spirits",                    icon="ability_ardenweald_hunter.jpg")
HUNTER_BEASTMASTERY.add_spell( spell_id=193530, cooldown=180, duration=20,                  name="Aspect of the Wild",              icon="spell_nature_protectionformnature.jpg")
HUNTER_BEASTMASTERY.add_spell( spell_id=19574,  cooldown=30,  duration=15, color="#e6960f", name="Bestial Wrath",                   icon="ability_druid_ferociousbite.jpg",           show=False)
HUNTER_MARKSMANSHIP.add_spell( spell_id=288613, cooldown=120, duration=15,                  name="Trueshot",                        icon="ability_trueshot.jpg",                      show=False)
#################################################################################################################################################################################################
#   Rouge
#################################################################################################################################################################################################
#   Priest
PRIEST.add_spell(              spell_id=10060,  cooldown=120, duration=20, color="#1fbcd1", name="Power Infusion",                  icon="spell_holy_powerinfusion.jpg",              show=False)
PRIEST_DISCIPLINE.add_spell(   spell_id=62618,  cooldown=180, duration=10, color="#b3ad91", name="Power Word: Barrier",             icon="spell_holy_powerwordbarrier.jpg")
PRIEST_DISCIPLINE.add_spell(   spell_id=109964, cooldown=60,  duration=10, color="#d7abdb", name="Spirit Shell",                    icon="ability_shaman_astralshift.jpg")
PRIEST_DISCIPLINE.add_spell(   spell_id=47536,  cooldown=90,  duration=8,                   name="Rapture",                         icon="spell_holy_rapture.jpg",                    show=False)
PRIEST_DISCIPLINE.add_spell(   spell_id=246287, cooldown=90,                                name="Evangelism",                      icon="spell_holy_divineillumination.jpg",         show=False)
PRIEST_HOLY.add_spell(         spell_id=64843,  cooldown=180, duration=8, color="#d7abdb",  name="Divine Hymn",                     icon="spell_holy_divinehymn.jpg")
PRIEST_HOLY.add_spell(         spell_id=265202, cooldown=240,                               name="Holy Word: Salvation",            icon="ability_priest_archangel.jpg")
PRIEST_HOLY.add_spell(         spell_id=200183, cooldown=120, duration=20,                  name="Apotheosis",                      icon="ability_priest_ascension.jpg",              show=False)
#################################################################################################################################################################################################
# DK
DEATHKNIGHT.add_spell(         spell_id=51052,  cooldown=120, duration=10,                  name="Anti-Magic Zone",                 icon="spell_deathknight_antimagiczone.jpg",       show=False)
DEATHKNIGHT_UNHOLY.add_spell(  spell_id=42650,  cooldown=240, duration=30,                  name="Army of the Dead",                icon="spell_deathknight_armyofthedead.jpg")
DEATHKNIGHT_UNHOLY.add_spell(  spell_id=275699, cooldown=60,  duration=15,                  name="Apocalypse",                      icon="artifactability_unholydeathknight_deathsembrace.jpg", show=False)
#################################################################################################################################################################################################
#   Shaman
SHAMAN.add_spell(              spell_id=320674, cooldown=90,               color=COL_VENTR, name="Chain Harvest",                   icon="ability_revendreth_shaman.jpg",             show=False)
SHAMAN_ELEMENTAL.add_spell(    spell_id=191634, cooldown=60,               color="#00bfff", name="Stormkeeper",                     icon="ability_thunderking_lightningwhip.jpg")
SHAMAN_ELEMENTAL.add_spell(    spell_id=198067, cooldown=150,              color="#ffa500", name="Fire Elemental",                  icon="spell_fire_elemental_totem.jpg")
SHAMAN_ENHANCEMENT.add_spell(  spell_id=114051, cooldown=180,                               name="Ascendance",                      icon="spell_fire_elementaldevastation.jpg")
SHAMAN_ENHANCEMENT.add_spell(  spell_id=51533,  cooldown=120,                               name="Feral Spirit",                    icon="spell_shaman_feralspirit.jpg")
SHAMAN_RESTORATION.add_spell(  spell_id=108280, cooldown=180, duration=10,                  name="Healing Tide Totem",              icon="ability_shaman_healingtide.jpg")
SHAMAN_RESTORATION.add_spell(  spell_id=98008,  cooldown=180, duration=6,  color="#24b385", name="Spirit Link Totem",               icon="spell_shaman_spiritlink.jpg")
SHAMAN_RESTORATION.add_spell(  spell_id=16191,  cooldown=180, duration=8,  color=COL_MANA,  name="Mana Tide Totem",                 icon="spell_frost_summonwaterelemental.jpg",      show=False)
SHAMAN_RESTORATION.add_spell(  spell_id=207399, cooldown=300, duration=30, color="#d15a5a", name="Ancestral Protection Totem",      icon="spell_nature_reincarnation.jpg")
SHAMAN_RESTORATION.add_spell(  spell_id=114052, cooldown=180, duration=15,                  name="Ascendance",                      icon="spell_fire_elementaldevastation.jpg")
#################################################################################################################################################################################################
#   Mage
MAGE.add_spell(                spell_id=314791, cooldown=60,  duration=3,  color=COL_NF,    name="Shifting Power",                  icon="ability_ardenweald_mage.jpg",               show=False)
MAGE_FIRE.add_spell(           spell_id=190319, cooldown=60,  duration=10, color="#e3b02d", name="Combustion",                      icon="spell_fire_sealoffire.jpg")
MAGE_FIRE.add_spell(           spell_id=153561, cooldown=45,                                name="Meteor",                          icon="spell_mage_meteor.jpg",                     show=False)
#################################################################################################################################################################################################
#   Warlock
WARLOCK.add_spell(             spell_id=325640, cooldown=60,  duration=8,  color=COL_NF,    name="Soul Rot",                        icon="ability_ardenweald_warlock.jpg",            show=False)
WARLOCK_AFFLICTION.add_spell(  spell_id=205180, cooldown=180, duration=8,  color="#49ad6e", name="Summon Darkglare",                icon="inv_beholderwarlock.jpg")
WARLOCK_AFFLICTION.add_spell(  spell_id=113860, cooldown=120, duration=20, color="#c35ec4", name="Dark Soul: Misery",               icon="spell_warlock_soulburn.jpg")
WARLOCK_AFFLICTION.add_spell(  spell_id=205179, cooldown=45,  duration=16, color="#7833b0", name="Phantom Singularity",             icon="inv_enchant_voidsphere.jpg")
WARLOCK_DEMONOLOGY.add_spell(  spell_id=265187, cooldown=90,  duration=15, color="#9150ad", name="Summon Demonic Tyrant",           icon="inv_summondemonictyrant.jpg")
WARLOCK_DEMONOLOGY.add_spell(  spell_id=111898, cooldown=120, duration=17, color="#c46837", name="Grimoire: Felguard",              icon="spell_shadow_summonfelguard.jpg")
WARLOCK_DEMONOLOGY.add_spell(  spell_id=267217, cooldown=180, duration=15,                  name="Nether Portal",                   icon="inv_netherportal.jpg")
WARLOCK_DESTRUCTION.add_spell( spell_id=1122,   cooldown=180, duration=30, color="#91c45a", name="Summon Infernal",                 icon="spell_shadow_summoninfernal.jpg")
WARLOCK_DESTRUCTION.add_spell( spell_id=113858, cooldown=120, duration=20, color="#c35ec4", name="Dark Soul: Instability",          icon="spell_warlock_soulburn.jpg")
#################################################################################################################################################################################################
# Monk
MONK.add_spell(                spell_id=322109, cooldown=180,              color="#c72649", name="Touch of Death",                  icon="ability_monk_touchofdeath.jpg")
MONK.add_spell(                spell_id=115203, cooldown=360, duration=15,                  name="Fortifying Brew",                 icon="ability_monk_fortifyingale_new.jpg",        show=False)
MONK.add_spell(                spell_id=310454, cooldown=120, duration=30, color=COL_KYR,   name="Weapons of Order",                icon="ability_bastion_monk.jpg",                  show=False)
MONK_MISTWEAVER.add_spell(     spell_id=322118, cooldown=180, duration=3.5,                 name="Invoke Yu'lon, the Jade Serpent", icon="ability_monk_dragonkick.jpg")
MONK_MISTWEAVER.add_spell(     spell_id=115310, cooldown=180,              color="#00FF98", name="Revival",                         icon="spell_monk_revival.jpg")
MONK_MISTWEAVER.add_spell(     spell_id=325197, cooldown=180, duration=25, color="#e0bb36", name="Invoke Chi-Ji, the Red Crane",    icon="inv_pet_cranegod.jpg")
MONK_WINDWALKER.add_spell(     spell_id=123904, cooldown=120, duration=24, color="#8cdbbc", name="Invoke Xuen, the White Tiger",    icon="ability_monk_summontigerstatue.jpg")
MONK_WINDWALKER.add_spell(     spell_id=137639, cooldown=90,  duration=15, color="#be53db", name="Storm, Earth, and Fire",          icon="spell_nature_giftofthewild.jpg")
#################################################################################################################################################################################################
# Druid
DRUID.add_spell(               spell_id=323764, cooldown=120, duration=4,  color=COL_NF,    name="Convoke the Spirits",             icon="ability_ardenweald_druid.jpg",              show=False)
DRUID_RESTORATION.add_spell(   spell_id=197721, cooldown=90,  duration=8,  color="#7ec44d", name="Flourish",                        icon="spell_druid_wildburst.jpg",                 show=False)
DRUID_RESTORATION.add_spell(   spell_id=29166,  cooldown=180, duration=10, color="#3b97ed", name="Innervate",                       icon="spell_nature_lightning.jpg",                show=False)
DRUID_RESTORATION.add_spell(   spell_id=740,    cooldown=180, duration=6,  color="#6cbfd9", name="Tranquility",                     icon="/static/images/spells/spell_nature_tranquility.jpg")
DRUID_RESTORATION.add_spell(   spell_id=33891,  cooldown=180, duration=30,                  name="Incarnation: Tree of Life",       icon="ability_druid_improvedtreeform.jpg")
DRUID_BALANCE.add_spell(       spell_id=194223, cooldown=180, duration=20,                  name="Celestial Alignment",             icon="spell_nature_natureguardian.jpg")
DRUID_BALANCE.add_spell(       spell_id=102560, cooldown=180, duration=30,                  name="Incarnation: Chosen of Elune",    icon="spell_druid_incarnation.jpg")
DRUID_BALANCE.add_spell(       spell_id=205636, cooldown=60,  duration=10,                  name="Force of Nature",                 icon="ability_druid_forceofnature.jpg",           show=False)
DRUID_BALANCE.add_spell(       spell_id=202770, cooldown=60,  duration=8,                   name="Fury of Elune",                   icon="ability_druid_dreamstate.jpg",              show=False)
#################################################################################################################################################################################################
# DH
DEMONHUNTER.add_spell(         spell_id=306830, cooldown=60,               color=COL_KYR,   name="Elysian Decree",                  icon="ability_bastion_demonhunter.jpg")
DEMONHUNTER.add_spell(         spell_id=323639, cooldown=90,  duration=6,  color=COL_NF,    name="The Hunt",                        icon="ability_ardenweald_demonhunter.jpg")
DEMONHUNTER.add_spell(         spell_id=317009, cooldown=60,               color=COL_VENTR, name="Sinful Brand",                    icon="ability_revendreth_demonhunter.jpg")
DEMONHUNTER_HAVOC.add_spell(   spell_id=200166, cooldown=240, duration=30, color="#348540", name="Metamorphosis",                   icon="ability_demonhunter_metamorphasisdps.jpg")
DEMONHUNTER_HAVOC.add_spell(   spell_id=196718, cooldown=180, duration=8,                   name="Darkness",                        icon="ability_demonhunter_darkness.jpg",          show=False)
DEMONHUNTER_HAVOC.add_spell(   spell_id=196555, cooldown=180, duration=5,                   name="Netherwalk",                      icon="spell_warlock_demonsoul.jpg",               show=False)
#################################################################################################################################################################################################


################################################################################
#                                                                              #
#       POTIONS & TRINKETS                                                     #
#                                                                              #
################################################################################

_specs_dps = MDPS.specs + RDPS.specs
_specs_int = HEAL.specs + [PRIEST_SHADOW, SHAMAN_ELEMENTAL, MAGE, WARLOCK, DRUID_BALANCE]
_specs_agi = [HUNTER, ROGUE, SHAMAN_ENHANCEMENT, MONK_WINDWALKER, DRUID_FERAL, DEMONHUNTER]
_specs_str = [WARRIOR, PALADIN_RETRIBUTION, DEATHKNIGHT]

for s in HEAL.specs:
    s.add_spell(group=OTHER_POTION, spell_id=307161, cooldown=300, duration=10, color=COL_MANA,  name="Potion of Spiritual Clarity",  icon="inv_alchemy_80_elixir01orange.jpg")
    s.add_spell(group=OTHER_POTION, spell_id=307193, cooldown=300,              color=COL_MANA,  name="Spiritual Mana Potion",        icon="inv_alchemy_70_blue.jpg")
for s in _specs_int:
    s.add_spell(group=OTHER_POTION, spell_id=307162, cooldown=300, duration=25, color="#b576e8", name="Potion of Spectral Intellect", icon="trade_alchemy_potionc4.jpg")
for s in _specs_agi:
    s.add_spell(group=OTHER_POTION, spell_id=307159, cooldown=300, duration=25, color="#b576e8", name="Potion of Spectral Agility",   icon="trade_alchemy_potionc6.jpg")
for s in _specs_str:
    s.add_spell(group=OTHER_POTION, spell_id=307164, cooldown=300, duration=25, color="#b576e8", name="Potion of Spectral Strength",  icon="trade_alchemy_potionc2.jpg")
for s in SPECS:
    s.add_spell(group=OTHER_POTION, spell_id=307495, cooldown=300, duration=25, color="#57bd8b", name="Potion of Phantom Fire",       icon="inv_alchemy_90_combat1_green.jpg")

################################################################################
#
#       TRINKETS (and all class-potions)
#
################################################################################

# everyone
for s in SPECS:
    s.add_spell(group=OTHER_POTION, spell_id=6262,                                  name="Healthstone",                 icon="warlock_-healthstone.jpg", wowhead_data="item=5512")
    s.add_spell(group=OTHER_POTION, spell_id=307192, cooldown=300, color="#e35f5f", name="Spiritual Healing Potion",    icon="inv_alchemy_70_red.jpg",   wowhead_data="item=171267")

    # Raid Trinkets
    s.add_spell(group=OTHER_TRINKET, spell_id=345019, cooldown=90,                  name="Skulking Predator",           icon="inv_icon_wingbroken08d.jpg")
    s.add_spell(group=OTHER_TRINKET, spell_id=349857, cooldown=90,                  name="Dreadfire Vessel",            icon="inv_misc_trinket6oih_orb1.jpg", wowhead_data="item=184030&bonus=7359:6646")

    # Dungeon
    s.add_spell(group=OTHER_TRINKET, spell_id=330323, cooldown=180,                 name="Inscrutable Quantum Device",  icon="inv_trinket_80_titan02a.jpg", wowhead_data="item=179350&ilvl=226")
    s.add_spell(group=OTHER_TRINKET, spell_id=345539, cooldown=180, duration=35,    name="Empyreal Ordnance",           icon="spell_animabastion_nova.jpg", wowhead_data="item=180117&ilvl=226")
    s.add_spell(group=OTHER_TRINKET, spell_id=348139, cooldown=90,  duration=9,     name="Instructor's Divine Bell",    icon="inv_misc_bell_01.jpg",        wowhead_data="item=184842&ilvl=226")

    # Other Trinkets
    s.add_spell(group=OTHER_TRINKET, spell_id=345228, cooldown=60, duration=15,     name="Gladiator's Badge", icon="spell_holy_championsbond.jpg")

for s in _specs_int:
    s.add_spell(group=OTHER_TRINKET, spell_id=345801, cooldown=120, duration=15, name="Soulletting Ruby", icon="inv_jewelcrafting_livingruby_01.jpg",  wowhead_data="item=178809&bonus=7214:6652:1501:5884:6646")
    s.add_spell(group=OTHER_TRINKET, spell_id=345251, cooldown=60,  duration=15, name="Soul Igniter",     icon="inv_trinket_maldraxxus_02_yellow.jpg", wowhead_data="item=184019&bonus=7187:6652:1498:6646")

for s in _specs_agi:
    s.add_spell(group=OTHER_TRINKET, spell_id=345530, cooldown=90, duration=6,  name="Overcharged Anima Battery", icon="inv_battery_01.jpg",                   wowhead_data="item=180116&bonus=7359:6646")
    s.add_spell(group=OTHER_TRINKET, spell_id=345251, cooldown=60, duration=15, name="Soul Ignition",             icon="inv_trinket_maldraxxus_02_yellow.jpg", wowhead_data="item=184025&ilvl=226")

for spec in _specs_str:
    pass


ALL_SPELLS = list(WowSpell.all)


for spell in ALL_SPELLS:
    if spell.group.role is ROLE_ITEM:
        spell.show = False
