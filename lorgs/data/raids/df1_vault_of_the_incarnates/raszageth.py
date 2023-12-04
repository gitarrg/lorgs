"""08: Raszageth the Storm-Eater."""

from lorgs.models.raid_boss import RaidBoss


RASZAGETH = RaidBoss(id=2607, name="Raszageth the Storm-Eater", nick="Raszageth")


########################### Phase 1: Winds of Change ###########################

# Debuffs
RASZAGETH.add_cast(
    spell_id=381615,
    name="Static Charge / Fulminating Charge",
    duration=8,
    color="#297bcc",
    icon="spell_shaman_staticshock.jpg",
    variations=[
        378829,  # P2: Fulminating Charge
    ],
)

# Pushback
RASZAGETH.add_cast(
    spell_id=377612,
    name="Hurricane Wing / Tempest Wing",
    duration=6,
    color="#8f52cc",
    icon="ability_dragonriding_vigor01.jpg",
    variations=[
        385574,  # P2: Tempest Wing
    ],
)

# spread / adds
RASZAGETH.add_cast(
    spell_id=388643,
    name="Volatile Current",
    duration=3,
    color="#cca83d",
    icon="spell_nature_stormreach.jpg",
)

# Tank Hit
RASZAGETH.add_cast(
    spell_id=377658,
    name="Electrified Jaws",
    duration=33,
    color="#74dbf2",
    icon="ability_thunderking_balllightning.jpg",
    show=False,
)


##################### Intermission 1: The Primalist Strike #####################


############################ Phase 2: Surging Power ############################

RASZAGETH.add_buff(
    spell_id=388691,
    name="Stormsurge (Shield)",
    color="#cc3d3d",
    icon="ability_mage_shattershield.jpg",
)

####################### Intermission 2: The Vault Falters ######################

RASZAGETH.add_cast(
    spell_id=385068,
    name="Ball Lightning (Dodge)",
    duration=3,
    color="#3dccb4",
    icon="ability_monk_forcesphere.jpg",
)

RASZAGETH.add_cast(
    spell_id=389870,
    name="Storm Break (Teleport)",
    duration=3.5,
    color="#cca83d",
    icon="inv_10_elementalspiritfoozles_lightning.jpg",
)


########################### Phase 3: Storm Incarnate ###########################

RASZAGETH.add_cast(
    spell_id=386410,
    name="Thunderous Blast",
    duration=2,
    color="#b43dcc",
    icon="achievement_raidprimalist_raszageth.jpg",
)

RASZAGETH.add_cast(
    spell_id=399713,
    name="Magnetic Charge",
    duration=8,
    color="#3dcc6d",
    icon="ability_siege_engineer_magnetic_lasso.jpg",
)
