# -*- coding: utf-8 -*-
"""Warcaftlogs API Client."""

# IMPORT STANDARD LIBRARIES
import os
import typing

# IMPORT THIRD PARTY LIBRARIES
import aiohttp

# IMPORT LOCAL LIBRARIES
from lorgs.logger import logger, timeit


# error text we get from Warcraftlogs if a report does not exist.
ERROR_MESSAGE_INVALID_REPORT = "This report does not exist."


class InvalidReport(ValueError):
    """Exception raised when a report was not found"""


class WarcraftlogsClient:

    URL_API = "https://www.warcraftlogs.com/api/v2/client"
    URL_AUTH = "https://www.warcraftlogs.com/oauth/token"

    # reference used to provide a singelton interface.
    _instance: typing.Optional["WarcraftlogsClient"] = None

    @classmethod
    def get_instance(cls, *args, **kwargs) -> "WarcraftlogsClient":
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

    def __init__(self, client_id: str = "", client_secret: str = ""):
        super().__init__()

        # credentials
        self.client_id = client_id or os.getenv("WCL_CLIENT_ID")
        self.client_secret = client_secret or os.getenv("WCL_CLIENT_SECRET")
        self.headers: typing.Dict[str, str] = {}

        logger.info("NEW CLIENT: %s", self.client_id)
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
        logger.debug("Auth: %s", self.client_id)
        async with aiohttp.ClientSession() as session:
            async with session.post(url=self.URL_AUTH, data=data) as resp:

                try:
                    data = await resp.json()
                except Exception as e:
                    logger.error(resp)
                    raise e

        token = data.get("access_token", "")
        self.headers["Authorization"] = "Bearer " + token

    async def ensure_auth(self):
        if self.headers:
            return
        await self.update_auth_token()

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
        result = await self.query(query)
        info = result.get("rateLimitData", {})
        return info.get("limitPerHour", 0) - info.get("pointsSpentThisHour", 0)

    @timeit
    async def query(self, query):
        self._num_queries += 1
        logger.debug("Num Queries: %d", self._num_queries)

        query = f"""
        query {{
            {query}
        }}"""

        await self.ensure_auth()

        async with aiohttp.ClientSession() as session:
            async with session.get(url=self.URL_API, json={"query": query}, headers=self.headers) as resp:

                try:
                    result = await resp.json()
                except Exception as e:
                    logger.error(resp)
                    raise e

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

                        if message == ERROR_MESSAGE_INVALID_REPORT:
                            raise InvalidReport()

                        # TODO: find a way to not hardcode the error message
                        if message == "You do not have permission to view this report.":
                            raise PermissionError("Private Report!")

                        msg += "\n" + error.get("message") + " path:" + "/".join(error.get("path", []))

                    if msg:
                        print(query)
                        raise ValueError(msg)

                return result.get("data", {})

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
