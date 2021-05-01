# -*- coding: utf-8 -*-
"""Warcaftlogs API Client."""

# IMPORT STANDARD LIBRARIES
import asyncio
import hashlib
import os

# IMPORT THIRD PARTY LIBRARIES
import aiohttp

# IMPORT LOCAL LIBRARIES
from lorgs import models
from lorgs import utils
from lorgs.cache import Cache
from lorgs.logger import logger

#: int: cache time for the queries
CACHE_TIMEOUT = 60 * 60 * 2 # 2 hours minutes


def query_name(query):
    """str: short version of the query, used to logging."""
    query = query.replace("\n", "")
    query = query.replace(" ", "")
    query = query.replace("{", "/")
    query = query[:32] + "..."
    return query


class WarcraftlogsClient:

    URL_API = "https://www.warcraftlogs.com/api/v2/client"
    URL_AUTH = "https://www.warcraftlogs.com/oauth/token"

    _instance = None
    # <WarcraftlogsClient> or None: reference used to provide a singelton interface.

    @classmethod
    def get_instance(cls, *args, **kwargs):
        """Get an instance of the Client.

        This is a singleton-style wrapper,
        which will return an existing instance, if there is one,
        or create a new instance otherwise.

        Args:
            *args, **kwargs passed to the __init__

        Returns:
            <WarcraftlogsClient> instance.

        """
        if cls._instance is None:
            logger.debug("creating new WarcraftlogsClient")
            cls._instance = cls(*args, **kwargs)
        return cls._instance

    def __init__(self, client_id="", client_secret=""):
        super(WarcraftlogsClient, self).__init__()

        print("WarcraftlogsClient INIT")
        print("TEST: ", os.getenv("WCL_CLIENT_ID"))

        # credentials
        self.client_id = client_id or os.getenv("WCL_CLIENT_ID")
        self.client_secret = client_secret or os.getenv("WCL_CLIENT_SECRET")
        self.headers = {}

        self.cached = True
        self.cache = Cache

        self._num_queries = 0

    ################################
    #   Connection
    #

    async def update_auth_token(self):
        """Request a new Auth Token from Warcraftlogs."""
        data = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }
        logger.debug("Auth %s %s", self.client_id, self.client_secret)
        async with aiohttp.ClientSession() as session:
            async with session.post(url=self.URL_AUTH, data=data) as resp:

                try:
                    data = await resp.json()
                except Exception as e:
                    logger.error(resp)
                    raise e

        token = data.get("access_token", "")
        self.headers["Authorization"] = "Bearer " + token

    async def get_points_left(self):
        """Points left until we hit the rate limit."""
        query = """
        rateLimitData
        {
            pointsSpentThisHour
            limitPerHour
            pointsResetIn
        }
        """
        result = await self.query(query, usecache=False)
        info = result.get("rateLimitData", {})
        return info.get("limitPerHour", 0) - info.get("pointsSpentThisHour", 0)

    async def query(self, query, usecache=True):
        """

        TODO:
            - add a "@cached"-wrapper to clean this up

        """
        self._num_queries += 1
        logger.debug("Num Queries: %d", self._num_queries)

        usecache = self.cached and usecache

        query = f"""
        query {{
            {query}
        }}"""

        logger.debug("run query: %s", query_name(query))
        cache_key = "query/" + str(hashlib.md5(query.encode()).hexdigest())

        # caching
        if usecache:
            cached_result = usecache and self.cache.get(cache_key)
            if cached_result:
                logger.debug("using cached result")
                return cached_result

        logger.debug("not cached: %s", cache_key)

        # auth
        if not self.headers:
            await self.update_auth_token()

        async with aiohttp.ClientSession() as session:
            async with session.get(url=self.URL_API, json={"query": query}, headers=self.headers) as resp:

                try:
                    result = await resp.json()
                except Exception as e:
                    logger.error(resp)
                    raise(e)

                # some reports are private.. but still show up in rankings..
                # lets just see what happens
                # ----> it stops..
                # "You do not have permission to view this report"
                # TODO: figure out how to skip those reports..
                if result.get("error"):
                    raise ValueError(result.get("error"))

                if result.get("errors"):
                    msg = ""
                    for error in result.get("errors"):
                        message = error.get("message")

                        # this sometimes happens.. just skip those
                        if message == "You do not have permission to view this report.":
                            continue

                        msg += "\n" + error.get("message") + " path:" + "/".join(error.get("path", []))

                    if msg:
                        print(query)
                        raise ValueError(msg)

                data = result.get("data", {})
                if usecache:
                    self.cache.set(cache_key, data, timeout=CACHE_TIMEOUT)

                return data

    async def multiquery(self, queries):
        """Execute a list of queries as a batch.

        Args:
            queries(list[str]): the queries to run

        Returns:
            data[object]: the results in the same order

        """
        queries = [f"data{i}: {q}" for i, q in enumerate(queries)]
        query = "\n".join(queries)

        result = await self.query(query)
        return [result.get(f"data{i}") for i, _ in enumerate(queries)]
