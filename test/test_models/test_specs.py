import unittest
import dotenv
dotenv.load_dotenv() # pylint: disable=wrong-import-position
import mongoengine as me

# from lorgs import data
from lorgs import db
from lorgs.models.specs import WowRole
from lorgs.models.specs import WowClass
from lorgs.models.specs import WowSpec
from lorgs.data import init_specs


class TestRoles(unittest.TestCase):

    def test_icon_name(self):
        role = WowRole(name="Test")
        assert role.icon_name == "roles/test.jpg"

    def test_metric(self):
        role = WowRole(name="any spec")
        self.assertTrue(role.metric == "dps")

        role = WowRole(name="heal")
        self.assertTrue(role.metric == "hps")


class TestWowSpec(unittest.TestCase):

    def test_1(self):
        spec = data.PALADIN_HOLY
        assert spec.name == "Holy"
        assert spec.role == data.HEAL
        assert spec.wow_class.color == "#F48CBA"

    def test_2(self):
        spec = data.PALADIN_HOLY
        print(spec.spells)



if __name__ == '__main__':
    # unittest.main()

    # wow_class="Paladin", name="Holy"
    """
    HOLY_PALADIN = WowSpec.objects(role="Healer").first()
    for spec in WowSpec.objects(role="Healer"):
        print(repr(spec))
    """
    druid = WowClass.get(name="Druid")
    print(druid)

    for spec in druid.specs:
        print("\t", spec)

        for spell in spec.spells:
            print("\t\t", spell.group, spell, spell.show, spell.name)
    # print(druid.spells)
    # HOLY_PALADIN = WowSpec.objects(wow_class="Paladin", name="Holy").first()
    # print(HOLY_PALADIN.wow_class.color)
