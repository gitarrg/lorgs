

from lorgs import data
from lorgs import utils
from lorgs.models.specs import WowRole
from lorgs.models.specs import WowClass
from lorgs.models.specs import WowSpell
from lorgs.models.specs import WowSpec
from lorgs.cache import Cache

from lorgs.app import create_app

app = create_app()
Cache.set("spell_infos", {}, timeout=600)

# import pickle
wow_class = WowSpec.get(wow_class__name="Druid", name="Restoration")
spells = wow_class.spells

data = spells[:3]
Cache.set("test", data)

print("======== SAVED ========")

data = Cache.get("test")
print(data)

# with app.app_context():

