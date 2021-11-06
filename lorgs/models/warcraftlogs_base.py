
# for semi concrete classes
# pylint: disable=abstract-method

# IMPORT STANRD LIBRARIES
import abc
import re
import json
from typing import Type, TypeVar
import typing

# IMPORT THIRD PARTY LIBRARIES
import mongoengine as me

# IMPORT LOCAL LIBRARIES
from lorgs import utils
from lorgs.client import WarcraftlogsClient


VALID_OPS = ["eq", "lt", "lte", "gt", "gte"]
RE_KEY = fr"([\w\-]+)"  # expr to match the key/attr name. eg.: spec or role name
RE_OPS = fr"|".join(VALID_OPS)
RE_VAL = fr"\d+"

QUERY_ARG_RE = fr"(?P<key>{RE_KEY})\.((?P<op>{RE_OPS})\.)?(?P<value>{RE_VAL})"


def query_args_to_mongo(*query_args, prefix=""):
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
            op = "" # no operator suffix.

            # unless...
            # check for non existence, as there will be no field with value 0
            if value == 0:
                op = "exists"  # exists + value=0 --> non existant

        # assamble the parts
        parts = [prefix, key, op]
        parts = [part for part in parts if part] # filter eg.: no-prefix or no-op
        key = ".".join(parts)
        key = key.replace(".", "__")

        # update the dict
        mongo_kwargs[key] = value

    return mongo_kwargs


class wclclient_mixin:

    @property
    def client(self):
        return WarcraftlogsClient.get_instance()

    @abc.abstractmethod
    def get_query(self):
        """Get the Query string to fetch all information for this object."""
        return ""

    @staticmethod
    def combine_queries(*queries, op="or"):
        """Combine multiple queries.

        Example:
            >>> combine_queries("foo", "bar or baz", op="and")
            ((foo) and ("bar" or "baz"))

        """
        # combine all filters
        queries = [q for q in queries if q]   # filter out empty statements
        queries = [f"({q})" for q in queries] # wrap each into bracers

        queries_combined = f" {op} ".join(queries)
        return f"({queries_combined})"

    @abc.abstractmethod
    def process_query_result(self, query_result: dict):
        """Implement some custom logic here to process our results from the query."""

    async def load_many(self, objects, filters=None, chunk_size=0):
        """Load multiple objects at once.

        Args:
            objects(list[wclclient_mixin]): the objects to load
            filters(list[str], optional): extra argument to pass to the ``get_query``-call
            chunks_size[int, optional]: load in chunks of this size.

        """
        filters = filters or []

        # Generate the queries,
        # and filter out objects that generted no query (ussualy an indication that the item is already loaded)
        items = [(obj, obj.get_query()) for obj in objects]
        items = [(obj, q) for (obj, q) in items if q]
        if not items:
            return

        for chunk in utils.chunks(items, chunk_size):
            chunk_queries = [q for (_, q) in chunk]
            chunk_items = [o for (o, _) in chunk]

            query_results = await self.client.multiquery(chunk_queries)

            for obj, result in zip(chunk_items, query_results):
                obj.process_query_result(result)

    async def load(self, *args, **kwargs):
        return await self.load_many([self], *args, **kwargs)


class EmbeddedDocument(me.EmbeddedDocument, wclclient_mixin):
    """docstring for Base"""
    meta = {
        "allow_inheritance": True,
        "strict": False # ignore non existing properties
    }


T = TypeVar('T', bound="Document")


class Document(me.Document, wclclient_mixin):
    """docstring for Document"""

    meta = {
        'abstract': True,
        "strict": False # ignore non existing properties
    }

    # insert generated fields
    if typing.TYPE_CHECKING:
        objects: "me.queryset.QuerySetManager"

    @classmethod
    def get_or_create(cls: Type[T], **kwargs) -> T:
        obj = cls.objects(**kwargs).first()
        obj = obj or cls(**kwargs)
        return obj
