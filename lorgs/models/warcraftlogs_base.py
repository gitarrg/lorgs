# IMPORT STANRD LIBRARIES
import abc

# IMPORT THIRD PARTY LIBRARIES
import mongoengine as me

# IMPORT LOCAL LIBRARIES
from lorgs import utils
from lorgs.client import WarcraftlogsClient


class wclclient_mixin:

    @property
    def client(self):
        return WarcraftlogsClient.get_instance()

    @abc.abstractmethod
    def get_query(self, filters=None):
        """Get the Query string to fetch all information for this object."""
        return ""

    def process_query_result(self, query_result: dict):
        pass

    async def load_many(self, objects, filters=None, chunk_size=0):
        """Load multiple objects at once.

        Args:
            objects(list[wclclient_mixin]): the objects to load
            filters(list[str], optional): extra argument to pass to the ``get_query``-call
            chunks_size[int, optional]: load in chunks of this size.

        """
        if not objects:
            return

        for chunk in utils.chunks(objects, chunk_size):

            queries = [obj.get_query(filters or []) for obj in chunk]

            # for q in queries:
            #     print(q)

            query_result = await self.client.multiquery(queries)

            for obj, obj_data in zip(chunk, query_result):
                obj.process_query_result(obj_data)

    async def load(self, *args, **kwargs):
        return await self.load_many([self], *args, **kwargs)


class EmbeddedDocument(me.EmbeddedDocument, wclclient_mixin):
    """docstring for Base"""
    pass
    meta = {"allow_inheritance": True}



class Document(me.Document, wclclient_mixin):
    """docstring for Document"""

    meta = {
        'abstract': True,
    }

    @classmethod
    def get_or_create(cls, **kwargs):
        obj = cls.objects(**kwargs).first()
        obj = obj or cls(**kwargs)
        return obj
