"""Some Basic Deyugging Routes."""
# IMPORT STANDARD LIBRARIES
import datetime

# IMPORT THIRD PARTY LIBRARIES
import fastapi

# IMPORT LOCAL LIBRARIES
from lorgs.clients import sqs


router = fastapi.APIRouter(tags=["debug"])


@router.get("/ping")
def ping():
    """Basic Ping to check Server Status."""
    return {"reply": "Hi!", "time": datetime.datetime.utcnow().isoformat()}


@router.get("/ping/no_cache")
def ping_no_cache(response: fastapi.Response):
    """Basic Ping without Caching."""
    response.headers["Cache-Control"] = "no-cache"
    return {"reply": "Hi! No Cache", "time": datetime.datetime.utcnow().isoformat()}


@router.get("/ping/discord")
def ping_dc(response: fastapi.Response):
    """Basic Ping sendng a message via sqs to discord."""
    ts = datetime.datetime.utcnow().isoformat()
    payload = {"Text": "Hello", "time": ts}

    
    message = sqs.send_message(payload)
    payload["id"] = message["MessageId"]

    response.headers["Cache-Control"] = "no-cache"
    return payload


from lorgs.clients.redis_store import RedisModel
import typing
import time


class Item(RedisModel):

    # status: str = "old"
    value: str
    # items: dict[str, typing.Any] = {}
    # ttl: int = 30
    updated: datetime.datetime = datetime.datetime.now()




@router.get("/item/{key}")
def item_get(response: fastapi.Response, key: str):
    response.headers["Cache-Control"] = "no-cache"
    
    start = time.time()


    try:
        item = Item.get(key)
    except ValueError:
        return 404

    end = time.time()
    
    return {
        "item": item.dict(),
        "time": (end-start) * 1000,
    }


@router.put("/item/{key}")
def item_put(response: fastapi.Response, key: str, value: str):
    response.headers["Cache-Control"] = "no-cache"

    print("x", value)

    start = time.time()
    item = Item(key=key, value=value)
    item.save()
    end = time.time()

    return {
        "item": item.dict(),
        "time": (end-start) * 1000,
    }


