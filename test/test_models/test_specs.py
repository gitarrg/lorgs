

from lorgs import data
from lorgs import utils
from lorgs.models.specs import WowRole
from lorgs.models.specs import WowClass


"""
for wow_class in WowClass.all:
    print(wow_class)

    for spec in wow_class.specs:
        print("\t", spec)
"""


WARRIOR = WowClass.get(name="Warrior")

print(WARRIOR)
for spec in WARRIOR.specs:
    print("\t", spec, spec.icon_path)

    for spell in spec.spells:
        print("\t\t", spell.group, spell, spell.spell_name)




"""
for role in WowRole.all:
    print(role)
"""
