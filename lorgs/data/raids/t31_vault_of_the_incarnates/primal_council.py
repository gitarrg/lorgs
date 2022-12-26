"""03: The Primal Council."""

from lorgs.models.raid_boss import RaidBoss


PRIMAL_COUNCIL = RaidBoss(id=2590, name="The Primal Council")


# Kadros Icewrath:
PRIMAL_COUNCIL.add_cast(
    spell_id=373059,
    name="Primal Blizzard",
    duration=10,
    color="#29cccc",
    icon="spell_frost_arcticwinds.jpg",
)


# Dathea Windboss:
PRIMAL_COUNCIL.add_cast(
    spell_id=375331,
    name="Conductive Mark",
    color="#297bcc",
    duration=4,
    icon="spell_shaman_staticshock.jpg",
)


# Opalfang:
PRIMAL_COUNCIL.add_cast(
    spell_id=372322,  # +397134
    name="Earthen Pillar",
    duration=1.5,
    color="#bf8330",
    icon="ability_earthen_pillar.jpg",
)

# Firepath:
PRIMAL_COUNCIL.add_cast(
    spell_id=374038,
    name="Meteor Axes",
    duration=6,  # 6 sec + 15sec debuff
    color="#bf3030",
    icon="inv_offhand_1h_artifactdoomhammer_d_01.jpg",
)
