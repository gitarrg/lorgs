
import os
# pylint: disable=wrong-import-position,invalid-name
import dotenv
dotenv.load_dotenv()

os.environ["LORGS_CONFIG_NAME"] = "lorgs.config.HerokuProductionConfig"


from lorgs.app import create_app
from lorgs.cache import Cache


app = create_app()

client = Cache.cache._write_client

print(client)

for k in client.keys():
    print(k)
"""
"""
