
import asyncio
from lorgs import client
from lorgs.db import db
from lorgs.logger import logger
from lorgs.models.specs import WowRole, WowClass, WowSpec, WowSpell


WCL_CLIENT = client.WarcraftlogsClient()


CD_1_MIN = 1 * 60 # 60
CD_2_MIN = 2 * 60 # 120
CD_3_MIN = 3 * 60 # 180
CD_4_MIN = 4 * 60 # 240
CD_5_MIN = 5 * 60 # 300

# Some Colors
COL_NIGHTFAE = "#8d5ca1"
COL_VENTYR = "FireBrick"
COL_KYRIAN = "LightSkyBlue"
COL_NECROLORD = "MediumSeaGreen"

COL_MANA = "#5397ed"

_COLOR_MANA = COL_MANA
_COLOR_POT_MAINSTAT = "#b576e8"
_COLOR_POT_EXTRA = "#57bd8b"


COL_RED1 = "hsv(0deg 60% 50%)"





def load_spell_icons():
    logger.info("START")

    all_spells = WowSpell.query.all()
    asyncio.run(WCL_CLIENT.load_spell_icons(all_spells))

    # db.session.bulk_save_objects(all_spells)
    # db.session.commit()


def get_class(id, **kwargs):
    c = WowClass.get(id=id)
    c.update(**kwargs)
    return c

def get_spec(wow_class, wcl_id, **kwargs):
    spec = WowSpec.get(wow_class=wow_class, wcl_id=wcl_id)
    spec.update(**kwargs)
    return spec



def create_classes():
    logger.info("START")

    # WowClass.query.delete()
    # WowRole.query.delete()
    # #WowSpec.query.delete()

    ############################################################################
    #       ROLES
    #   (setting id's per hand to force order)
    #
    tank = WowRole.get(id=1, code="tank", name="Tank")
    heal = WowRole.get(id=2, code="heal", name="Healer")
    rdps = WowRole.get(id=3, code="rdps", name="Range")
    mdps = WowRole.get(id=4, code="mdps", name="Melee")
    # db.session.bulk_save_objects([tank, heal, mdps, rdps])
    # db.session.commit()

    ############################################################################
    #   CLASSES and SPECS
    #   (id's are based on wcl, because we need them for filters.)
    #
    #
    #   Warrior
    warrior = get_class(id=11, name="Warrior", color="#C69B6D")
    warrior_arms = get_spec(warrior, wcl_id=1, name="Arms", role=mdps)
    warrior_fury = get_spec(warrior, wcl_id=2, name="Fury", role=mdps)
    warrior_prot = get_spec(warrior, wcl_id=3, name="Protection", role=tank, short_name="Prot")

    ################################
    #   Paladin
    paladin = get_class(id=6, name="Paladin", color="#F48CBA")
    paladin_holy = get_spec(paladin, wcl_id=1, name="Holy", role=heal)
    paladin_protection = get_spec(paladin, wcl_id=2, name="Protection", role=tank, short_name="Prot")
    paladin_retribution = get_spec(paladin, wcl_id=3, name="Retribution", role=mdps, short_name="Ret")

    ################################
    # Hunter
    hunter = get_class(id=3, name="Hunter", color="#AAD372")
    hunter_beastmastery = get_spec(hunter, wcl_id=1, name="Beast Mastery", role=rdps)
    hunter_marksmanship = get_spec(hunter, wcl_id=2, name="Marksmanship", role=rdps)
    hunter_survival = get_spec(hunter, wcl_id=3, name="Survival", role=mdps)
    # db.session.add(hunter)
    ################################
    #   Rouge
    rogue = get_class(id=8, name="Rogue", color="#FFF468")
    rogue_assassination = get_spec(rogue, wcl_id=1, name="Assassination", role=mdps, short_name="Assa")
    rogue_outlaw = get_spec(rogue, wcl_id=2, name="Outlaw", role=mdps)
    rogue_subtlety = get_spec(rogue, wcl_id=3, name="Subtlety", role=mdps)
    ################################
    #   Priest
    priest = get_class(id=7, name="Priest", color="#FFFFFF")
    priest_discipline = get_spec(priest, wcl_id=1, name="Discipline", role=heal, short_name="Disc")
    priest_holy = get_spec(priest, wcl_id=2, name="Holy", role=heal)
    priest_shadow = get_spec(priest, wcl_id=3, name="Shadow", role=rdps)

    ################################
    # DK
    deathknight = get_class(id=1, name="Death Knight", color="#C41E3A")
    deathknight_blood = get_spec(deathknight, wcl_id=1, name="Blood", role=tank)
    deathknight_frost = get_spec(deathknight, wcl_id=1, name="Frost", role=mdps)
    deathknight_unholy = get_spec(deathknight, wcl_id=1, name="Unholy", role=mdps)

    ################################
    #   Shaman
    shaman = get_class(id=9, name="Shaman", color="#0070DD")
    shaman_elemental = get_spec(shaman, wcl_id=1, name="Elemental", role=rdps)
    shaman_enhancement = get_spec(shaman, wcl_id=2, name="Enhancement", role=mdps)
    shaman_restoration = get_spec(shaman, wcl_id=3, name="Restoration", role=heal)
    shaman_restoration.short_name = "Resto"

    ################################
    #   Mage
    mage = get_class(id=4, name="Mage", color="#3FC7EB")
    mage_arcane = get_spec(mage, wcl_id=1, name="Arcane", role=rdps)
    mage_fire = get_spec(mage, wcl_id=2, name="Fire", role=rdps)
    mage_frost = get_spec(mage, wcl_id=3, name="Frost", role=rdps)

    ################################
    #   Warlock
    warlock = get_class(id=10, name="Warlock", color="#8788EE")
    warlock_affliction = get_spec(warlock, wcl_id=1, name="Affliction", role=rdps, short_name="Aff")
    warlock_demonology = get_spec(warlock, wcl_id=2, name="Demonology", role=rdps, short_name="Demo")
    warlock_destruction = get_spec(warlock, wcl_id=3, name="Destruction", role=rdps)

    ################################
    # Monk
    monk = get_class(id=5, name="Monk", color="#00FF98")
    monk_brewmaster = get_spec(monk, wcl_id=1, name="Brewmaster", role=tank)
    monk_mistweaver = get_spec(monk, wcl_id=2, name="Mistweaver", role=heal)
    monk_windwalker = get_spec(monk, wcl_id=3, name="Windwalker", role=mdps)

    ################################
    # Druid
    druid = get_class(id=2, name="Druid", color="#FF7C0A")
    druid_balance = get_spec(druid, wcl_id=1, name="Balance", role=rdps)
    druid_feral = get_spec(druid, wcl_id=2, name="Feral", role=mdps)
    druid_guardian = get_spec(druid, wcl_id=3, name="Guardian", role=tank)
    druid_restoration = get_spec(druid, wcl_id=4, name="Restoration", role=heal)
    druid_restoration.short_name = "Resto"

    ################################
    # DH
    demonhunter = get_class(id=12, name="Demon Hunter", color="#A330C9")
    demonhunter_havoc = get_spec(demonhunter, wcl_id=1, name="Havoc", role=mdps)
    demonhunter_vengeance = get_spec(demonhunter, wcl_id=2, name="Vengeance", role=tank)

    # sorry guys...
    warrior_prot.supported = False
    paladin_protection.supported = False
    deathknight_blood.supported = False
    monk_brewmaster.supported = False
    druid_guardian.supported = False
    demonhunter_vengeance.supported = False

    # mdps
    warrior_arms.supported = False
    hunter_survival.supported = False
    rogue_assassination.supported = False
    rogue_subtlety.supported = False
    rogue_outlaw.supported = False
    deathknight_frost.supported = False
    druid_feral.supported = False

    # rdps
    priest_shadow.supported = False
    mage_arcane.supported = False
    mage_frost.supported = False

    ############################################################################
    #   SPELLS
    #
    #

    warrior.add_spell(spell_id=325886, cooldown=90, duration=12, color=COL_NIGHTFAE) # Nightfae: Ancient Aftershock
    warrior.add_spell(spell_id=97462, cooldown=180, duration=10, show=False) # Rally Cry
    # warrior_fury.add_spell(spell_id=107574, cooldown=90, duration=20) # Avatar
    warrior_fury.add_spell(spell_id=1719, cooldown=60, duration=10) # Recklessness # reduced by Anger Management
    warrior_fury.add_spell(spell_id=46924, cooldown=60, duration=4) # Bladestorm

    # paladin.add_spell(spell_id=105809, cooldown=180, duration=20, show=False) # Holy Avenger
    paladin.add_spell(spell_id=304971, cooldown=CD_1_MIN, show=False, color=COL_KYRIAN) # Covenant: Divine Toll
    paladin.add_spell(spell_id=316958, cooldown=CD_4_MIN, duration=30, color=COL_VENTYR) # Covenant: Ashen Hallow
    paladin.add_spell(spell_id=31884, cooldown=CD_2_MIN, duration=20) # Wings
    paladin_holy.add_spell(spell_id=31821, cooldown=CD_3_MIN, duration=8, color="#dc65f5") # Aura Mastery

    hunter.add_spell(spell_id=328231, cooldown=120, duration=15, color=COL_NIGHTFAE) # Covenant: Wild Spirits
    hunter_beastmastery.add_spell(spell_id=193530, cooldown=180, duration=20) # Aspect of the Wild
    hunter_beastmastery.add_spell(spell_id=19574, cooldown=30, duration=15, show=False, color="#9c8954") # Bestial Wrath
    # hunter_survival.add_spell(spell_id=266779, cooldown=120, duration=20) # Coordinated Assault
    hunter_marksmanship.add_spell(spell_id=288613, cooldown=120, duration=15, show=False) # Trueshot

    # Rogue

    # Priest
    priest.add_spell(spell_id=10060, cooldown=CD_2_MIN, duration=20, show=False, color="#1fbcd1") # Power Infusion
    # priest_shadow.add_spell(spell_id=34433, cooldown=180, duration=15) # Shadowfiend
    # priest_shadow.add_spell(spell_id=228260, cooldown=90) # Void Erruption
    # priest_discipline.add_spell(spell_id=34433, cooldown=180, duration=15, show=False) # Shadowfiend
    #TODO: add mindbender?
    priest_discipline.add_spell(spell_id=62618,  cooldown=180, duration=10, color="#b3ad91")  #Power Word: Cuddle
    priest_discipline.add_spell(spell_id=109964,  cooldown=60, duration=10, color="#d7abdb")  # Spirit Shell
    priest_discipline.add_spell(spell_id=47536,  cooldown=90, duration=8, show=False)  # Rapture
    priest_discipline.add_spell(spell_id=246287,  cooldown=90, show=False)  # Evengelism
    priest_holy.add_spell(spell_id=64843, cooldown=180, duration=8, color="#d7abdb") # Hymn
    priest_holy.add_spell(spell_id=265202, cooldown=240) # Savl (not showing CD, because dynamic)
    priest_holy.add_spell(spell_id=200183, cooldown=120, duration=20, show=False) # Apotheosis

    # DK
    deathknight.add_spell(spell_id=51052, cooldown=120, duration=10, show=False)  # Anti-Magic Zone
    deathknight_unholy.add_spell(spell_id=42650, cooldown=4*60, duration=30)  # Army (usually 4min with talent)
    deathknight_unholy.add_spell(spell_id=275699, cooldown=60, duration=15, show=False)  # Apocalypse (90sec -> 60sec talent)

    # Shamans
    # shaman.add_spell(spell_id=326059, cooldown=45, show=False, color=COL_NECROLORD)  # Necro: Primordial Wave
    shaman.add_spell(spell_id=320674, cooldown=90, show=False, color=COL_VENTYR)  # Ventyr: Chain Harvest
    shaman_elemental.add_spell(spell_id=191634, cooldown=60, show=True, color="DeepSkyBlue")  # Stormkeeper
    shaman_elemental.add_spell(spell_id=198067, cooldown=150, show=True, color="DarkOrange")  # Fire Elemental

    shaman_enhancement.add_spell(spell_id=114051, cooldown=CD_3_MIN, show=True)  # Ascendance
    shaman_enhancement.add_spell(spell_id=51533, cooldown=CD_2_MIN, show=True)  # Feral Spirit

    shaman_restoration.add_spell(spell_id=108280, cooldown=180, duration=10) # Healing Tide
    shaman_restoration.add_spell(spell_id=98008,  cooldown=180, duration=6, color="#24b385")  # Spirit Link
    shaman_restoration.add_spell(spell_id=16191,  cooldown=180, duration=8, show=False, color=COL_MANA)  # Mana Tide
    shaman_restoration.add_spell(spell_id=207399,  cooldown=300, duration=30, color="#d15a5a")  # Ahnk totem
    shaman_restoration.add_spell(spell_id=114052,  cooldown=180, duration=15)  # Ascendance

    # Mage
    mage.add_spell(spell_id=314791, cooldown=60, duration=3.1, show=False, color=COL_NIGHTFAE) # Shifting Power
    mage_fire.add_spell(spell_id=190319, cooldown=60, duration=10, color="#e3b02d") # Combustion
    mage_fire.add_spell(spell_id=153561, cooldown=45, show=False) # Meteor

    # Warlock
    warlock.add_spell(spell_id=325640, cooldown=60, duration=8, show=False, color=COL_NIGHTFAE) # Soulrot

    warlock_affliction.add_spell(spell_id=205180, cooldown=180, duration=8, color="#49ad6e") # Darkglare
    warlock_affliction.add_spell(spell_id=113860, cooldown=120, duration=20, color="#c35ec4") # Dark Soul: Misery
    warlock_affliction.add_spell(spell_id=205179, cooldown=45, duration=16, color="#7833b0") # PS

    warlock_demonology.add_spell(spell_id=265187, cooldown=90, duration=15, color="#9150ad") # Tyrant
    warlock_demonology.add_spell(spell_id=111898, cooldown=120, duration=17, color="#c46837") # Felguard
    warlock_demonology.add_spell(spell_id=267217, cooldown=180, duration=15) # Netherportal

    warlock_destruction.add_spell(spell_id=1122, cooldown=180, duration=30, color="#91c45a") # Infernal
    warlock_destruction.add_spell(spell_id=113858, cooldown=120, duration=20, color="#c35ec4") # Dark Soul: Instability

    # Monk
    monk.add_spell(spell_id=322109, cooldown=180, color="#c72649") # Touch of Death
    monk.add_spell(spell_id=115203, cooldown=360, duration=15, show=False) # Fort Brew
    monk.add_spell(spell_id=310454, cooldown=120, duration=30, show=False, color=COL_KYRIAN) # Weapons of Order

    monk_mistweaver.add_spell(spell_id=322118, cooldown=180, duration=3.5) # Yulon
    monk_mistweaver.add_spell(spell_id=115310, cooldown=180, color="#00FF98") # Revival
    monk_mistweaver.add_spell(spell_id=325197, cooldown=180, duration=25, color="#e0bb36") # Chiji

    monk_windwalker.add_spell(spell_id=123904, cooldown=120, duration=24, color="#8cdbbc") # Xuen
    monk_windwalker.add_spell(spell_id=137639, cooldown=90, duration=15, color="#be53db") # Storm, Earth and Fire

    # Druid
    druid.add_spell(spell_id=323764, cooldown=120, duration=4, show=False, color=COL_NIGHTFAE)  # Convoke
    druid_restoration.add_spell(spell_id=197721, cooldown=90, duration=8, show=False, color="#7ec44d") # Flourish
    druid_restoration.add_spell(spell_id=29166, cooldown=180, duration=10, show=False, color="#3b97ed") # Innervate
    druid_restoration.add_spell(spell_id=740, cooldown=180, duration=6, color="#6cbfd9") # Tranquility
    druid_restoration.add_spell(spell_id=33891, cooldown=180, duration=30) # Tree of Life

    druid_balance.add_spell(spell_id=194223, cooldown=180, duration=20) # Celestrial
    druid_balance.add_spell(spell_id=102560, cooldown=180, duration=30) # Incarnation
    druid_balance.add_spell(spell_id=205636, cooldown=60, duration=10, show=False) # Treants
    druid_balance.add_spell(spell_id=202770, cooldown=60, duration=8, show=False) # Fury of Elune

    # DH
    demonhunter.add_spell(spell_id=306830, cooldown=60, color=COL_KYRIAN) # Elysian Decree
    demonhunter.add_spell(spell_id=323639, cooldown=90, duration=6, color=COL_NIGHTFAE) # The Hunt
    demonhunter.add_spell(spell_id=317009, cooldown=60, color=COL_VENTYR) # Sinful Brand

    demonhunter_havoc.add_spell(spell_id=200166, cooldown=CD_4_MIN, duration=30, color="#348540", icon="ability_demonhunter_metamorphasisdps.jpg") # Meta
    demonhunter_havoc.add_spell(spell_id=196718, cooldown=180, duration=8, show=False) # Darkness
    demonhunter_havoc.add_spell(spell_id=196555, cooldown=180, duration=5, show=False) # Netherwalk

    db.session.add(paladin)

    return


def create_potions():
    pass




def create():
    create_classes()
    create_potions()


def load():
    load_spell_icons()



if __name__ == '__main__':
    main()
