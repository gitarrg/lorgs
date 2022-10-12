"""07: Broodkeeper Diurna."""

from lorgs.models.raid_boss import RaidBoss


DIURNA = RaidBoss(id=2614, name="Broodkeeper Diurna", nick="Diurna")

DIURNA.add_cast(
    spell_id=375871, name="Wildfire", duration= 1.5 + 9,
    color="#bf3030", icon="spell_shadow_rainoffire.jpg",
)

DIURNA.add_cast(
    spell_id=388716, name="Icy Shroud",
    duration= 1.5 + 5, # variable duration for debuff to be healed off
    color="#60afbf", icon="spell_fire_blueflamering.jpg",
    variations=[
        388918, # p2
    ],
)

DIURNA.add_cast(
    spell_id=380175, name="Greatstaff of the Broodkeeper",
    color="#bf60bf", icon="inv_staff_2h_broodkeeper_d_01.jpg",
    duration=1+9,
)

DIURNA.add_cast(
    spell_id=375829, name="Clutchwatcher's Rage",
    color="#30bf30", icon="inv_staff_2h_broodkeeper_d_01.jpg",
    duration=1+9,
    show=False,
)

DIURNA.add_buff(
    spell_id=375879, name="Broodkeeper's Fury",
    druation=0, # permanent, stacking up
    icon="ability_warrior_focusedrage.jpg",
)
