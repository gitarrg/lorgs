from lorgs.data.classes import *
from lorgs.models.wow_trinket import WowTrinket


WowTrinket(
    *AGI_SPECS,
    spell_id=265954,
    color="#d3d01a",
    cooldown=90,
    name="My'das Talisman",
    icon="inv_offhand_draenei_a_02.jpg",
    item=158319,
    ilvl=483,
)


WowTrinket(
    *INT_SPECS,
    spell_id=268998,
    event_type="applybuff",
    color="#8434df",
    cooldown=90,
    name="Balefire Branch",
    icon="inv_staff_26.jpg",
    show=False,
    item=159630,
    ilvl=483,
)


WowTrinket(
    *STR_SPECS,
    spell_id=268836,
    event_type="applybuff",
    color="#ba5bb5",
    cooldown=90,
    duration=18,
    name="Vial of Animated Blood",
    icon="inv_misc_food_legion_leyblood.jpg",
    item=159625,
    ilvl=372,
    query=False,
)
