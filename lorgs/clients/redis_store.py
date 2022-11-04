"""Basic Client to store Objects in a Redis DB."""

# IMPORT STANDARD LIBRARIES
import os
import json
import typing

# IMPORT THIRD PARTY LIBRARIES
import pydantic
import redis


REDIS_URL = os.getenv("REDIS_URL") or "redis://localhost:6379"


redis_client = redis.from_url(REDIS_URL)


T = typing.TypeVar("T", bound="RedisModel")


class RedisModel(pydantic.BaseModel):

    key: str = pydantic.Field(exclude=True)

    ttl: int = pydantic.Field(exclude=True, default=0)

    @property
    def client(self) -> redis.Redis:
        """Shared Redis Client."""
        return redis_client

    @classmethod
    def get_key(cls, key: str) -> str:
        """Generate a full Key (with Prefix)"""
        prefix = cls.__name__.lower()
        if prefix:
            key = f"{prefix}:{key}"
        return key

    def save(self) -> None:
        """Save the Object."""
        key = self.get_key(self.key)

        # Use pydantics json encoder to convert complex types (eg.: datetime)
        data = json.loads(self.json())

        self.client.json().set(name=key, path=".", obj=data)

        if self.ttl:
            self.client.expire(key, self.ttl)

    def set(self, **kwargs: typing.Any) -> None:
        """Update values on the Object,
       
        Todo:
            reload/update the instance itself
        """
        key = self.get_key(self.key)

        for path, value in kwargs.items():
            if not path.startswith("."):
                path = f".{path}"
            self.client.json().set(name=key, path=path, obj=value)

    @typing.overload
    @classmethod
    def get(cls: typing.Type[T], key: str, create: typing.Literal[True]) -> T:
        ...

    @typing.overload
    @classmethod
    def get(cls: typing.Type[T], key: str, create: bool = False) -> typing.Optional[T]:
        ...

    @classmethod
    def get(cls: typing.Type[T], key: str, create=False) -> typing.Optional[T]:
        """Get a Object using its Key."""
        full_key = cls.get_key(key)
        data = redis_client.json().get(full_key) or {}

        if not data and not create:
            return None
            # raise ValueError("Item not found.")

        data["key"] = key
        return cls.parse_obj(data)
