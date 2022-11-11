import json
import os
from uuid import uuid4

import dotenv
from pymongo import MongoClient

from lorgs.logger import Timer, timeit
from lorgs.models.user import User


dotenv.load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

mongo_client: MongoClient = MongoClient(MONGO_URI)
# mongo_db = mongo_client[""]


def get_mongo_users(limit=0) -> list[dict]:
    mongo_db = mongo_client["lorgs_9_2"]
    users = mongo_db["user"]
    return users.find(limit=limit)  # type: ignore


def main() -> None:

    table = User.get_table()
    with table.batch_writer() as batch:
        for data in get_mongo_users(limit=0):

            data = {k: v for k, v in data.items() if v}
            data["discord_id"] = data.get("discord_id") or data.get("discord_tag") or f"U-{uuid4()}"

            print("D", data)

            user = User.construct(**data)
            print("U", user)

            item = json.loads(user.json(exclude_unset=True))
            item.update(user.get_keys(**item))
            print("I", item)

            batch.put_item(Item=item)
            continue


if __name__ == "__main__":
    main()
