"""03: The Primal Council."""

from lorgs.models.raid_boss import RaidBoss


PRIMAL_COUNCIL = RaidBoss(id=2590, name="The Primal Council")


PRIMAL_COUNCIL.add_cast(
    spell_id=373059, name="Primal Blizzard", duration=10,
    color="#308fbf", icon="ability_skyreach_four_wind.jpg",
)

# Conductive Mark
# 371624
# (no spell.. only raid debuff)

PRIMAL_COUNCIL.add_cast(
    spell_id=372322, name="Earthen Pillar", duration=1.5,
    color="#bf8330", icon="ability_earthen_pillar.jpg",
)

PRIMAL_COUNCIL.add_cast(
    spell_id=374038, name="Meteor Axes", duration=6,  # 6 sec + 15sec debuff
    color="#bf3030", icon="inv_offhand_1h_artifactdoomhammer_d_01.jpg",
)
