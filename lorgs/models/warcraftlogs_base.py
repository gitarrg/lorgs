# IMPORT STANRD LIBRARIES
from typing import Type, TypeVar
import abc
import asyncio
import json
import re
import typing

# IMPORT THIRD PARTY LIBRARIES
import mongoengine as me

# IMPORT LOCAL LIBRARIES
from lorgs.clients.wcl import WarcraftlogsClient


VALID_OPS = ["eq", "lt", "lte", "gt", "gte"]
RE_KEY = r"([\w\-]+)"  # expr to match the key/attr name. eg.: spec or role name
RE_OPS = r"|".join(VALID_OPS)
RE_VAL = r"\d+"

QUERY_ARG_RE = rf"(?P<key>{RE_KEY})\.((?P<op>{RE_OPS})\.)?(?P<value>{RE_VAL})"


def query_args_to_mongo(*query_args: str, prefix="") -> dict[str, str]:
    """Takes a list of query strings and converts them into mongoengine-style kwargs.

    Args:
        query_args(list[str]): the arguments to convert.
            Expected format is: "key:op:value"
        prefix(str, optional): prefix to add to the keys

    Example:
        >>> query_args = ["tank.2", "heal.lt.5"]
        >>> query_args_to_mongo(*query_args, prefix="something)
        {
            'something__tank': '2',
            'something__heal__lt': '5'
        }

    """
    mongo_kwargs = {}

    for arg in query_args:

        m = re.match(QUERY_ARG_RE, arg)
        if not m:
            print("invalid query arg", arg)
            continue

        # split re.match
        key = m.group("key")
        op = m.group("op")
        value = json.loads(m.group("value"))

        # special case for equals
        if op == "eq":
            op = ""  # no operator suffix.

            # unless...
            # check for non existence, as there will be no field with value 0
            if value == 0:
                op = "exists"  # exists + value=0 --> non existant

        # assamble the parts
        parts = [prefix, key, op]
        parts = [part for part in parts if part]  # filter eg.: no-prefix or no-op
        key = ".".join(parts)
        key = key.replace(".", "__")

        # update the dict
        mongo_kwargs[key] = value

    return mongo_kwargs


W = TypeVar("W", bound="wclclient_mixin")


class wclclient_mixin:
    @property
    def client(self) -> WarcraftlogsClient:
        return WarcraftlogsClient.get_instance()

    @abc.abstractmethod
    def get_query(self) -> str:
        """Get the Query string to fetch all information for this object."""
        return ""

    @staticmethod
    def combine_queries(*queries: str, op="or") -> str:
        """Combine multiple queries.

        Example:
            >>> combine_queries("foo", "bar or baz", op="and")
            ((foo) and ("bar" or "baz"))

        """
        # combine all filters
        queries = [q for q in queries if q]  # type: ignore # filter out empty statements
        queries = [f"({q})" for q in queries]  # type: ignore # wrap each into bracers

        queries_combined = f" {op} ".join(queries)
        return f"({queries_combined})"

    @abc.abstractmethod
    def process_query_result(self, **query_result: typing.Any) -> None:
        """Implement some custom logic here to process our results from the query."""

    async def load_many(self: W, items: list[W], raise_errors=False) -> None:
        """Load multiple objects at once.

        Args:
            items(list[wclclient_mixin]): the objects to load
            chunks_size[int, optional]: load in chunks of this size.

        """
        tasks = [item.load(raise_errors=raise_errors) for item in items]
        await asyncio.gather(*tasks)

    async def load(self, raise_errors=False) -> None:
        query = self.get_query()
        if not query:
            return

        result = await self.client.query(query=query, raise_errors=raise_errors)

        if result:
            self.process_query_result(**result)


class EmbeddedDocument(me.EmbeddedDocument, wclclient_mixin):
    """docstring for Base"""

    meta = {"allow_inheritance": True, "strict": False}  # ignore non existing properties


T = TypeVar("T", bound="Document")


class Document(me.Document, wclclient_mixin):
    """docstring for Document"""

    meta = {"abstract": True, "strict": False}  # ignore non existing properties

    @classmethod
    def get_or_create(cls: Type[T], **kwargs: typing.Any) -> T:
        obj = cls.objects(**kwargs).first()
        obj = obj or cls(**kwargs)
        return obj  # type: ignore
