# -*- coding: utf-8 -*-
"""Warcaftlogs API Client."""

# IMPORT STANDARD LIBRARIES
import asyncio
import os
import typing

# IMPORT THIRD PARTY LIBRARIES
import aiohttp

# IMPORT LOCAL LIBRARIES
from lorgs.logger import logger, timeit


# error text we get from Warcraftlogs if a report does not exist.
ERROR_MESSAGE_INVALID_REPORT = "This report does not exist."


class InvalidReport(ValueError):
    """Exception raised when a report was not found."""


class BaseClient:

    _sem = asyncio.Semaphore(value=10)
    """Semaphore used to control the number of parallel Requests."""

    def __init__(self) -> None:
        self.session: typing.Optional[aiohttp.ClientSession] = None
        self.headers: dict[str, typing.Any] = {}

    async def ensure_auth(self) -> None:
        pass

    @timeit
    async def query(self, url: str, query: str) -> typing.Any:
        """Executes a "query" to "url".

        reuses a shared ClientSession and limits the maximum number of
        parallel connections

        Args:
            query (str): the query to execute
        """
        self.session = self.session or aiohttp.ClientSession()
        async with self._sem:
            await self.ensure_auth()
            async with self.session.get(url=url, json={"query": query}, headers=self.headers) as resp:
                resp.raise_for_status()
                return await resp.json()


class WarcraftlogsClient(BaseClient):

    URL_API = "https://www.warcraftlogs.com/api/v2/client"
    URL_AUTH = "https://www.warcraftlogs.com/oauth/token"

    # reference used to provide a singelton interface.
    _instance: typing.Optional["WarcraftlogsClient"] = None

    @classmethod
    def get_instance(cls, *args: typing.Any, **kwargs: typing.Any) -> "WarcraftlogsClient":
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

    def __init__(self, client_id: str = "", client_secret: str = "") -> None:
        super().__init__()

        # credentials
        self.client_id = client_id or os.getenv("WCL_CLIENT_ID")
        self.client_secret = client_secret or os.getenv("WCL_CLIENT_SECRET")
        self.headers: dict[str, str] = {}

        auth_token = os.getenv("WCL_AUTH_TOKEN")
        if auth_token:
            self.headers["Authorization"] = "Bearer " + auth_token

        logger.info("NEW CLIENT: %s", self.client_id)
        self._num_queries = 0

    ################################
    #   Connection
    #

    async def update_auth_token(self) -> None:
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
                    response: dict[str, str] = await resp.json()
                except Exception as e:
                    logger.error(resp.text())
                    raise e

        token = response.get("access_token", "")
        self.headers["Authorization"] = "Bearer " + token

    async def ensure_auth(self) -> None:
        if self.headers.get("Authorization"):
            return
        await self.update_auth_token()

    async def get_points_left(self) -> int:
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
        info: dict[str, int] = result.get("rateLimitData", {})
        return info.get("limitPerHour", 0) - info.get("pointsSpentThisHour", 0)

    def raise_errors(self, result: dict[str, typing.Any]) -> None:
        if result.get("error"):
            raise ValueError(result.get("error"))

        errors = result.get("errors") or []
        if errors:
            msg = ""
            for error in errors:
                message = error.get("message")

                if message == "This report does not exist.":
                    raise InvalidReport()
                if message == "You do not have permission to view this report.":
                    # some reports are private.. but still show up in rankings..
                    raise PermissionError("Private Report!")

                msg += "\n" + error.get("message") + " path:" + "/".join(error.get("path", []))
            if msg:
                # print(query)
                raise ValueError(msg)

    async def query(self, query: str, raise_errors=True) -> dict[str, typing.Any]:

        # Format Inputs
        if not query:
            return {}
        query = f"query {{ {query} }}"

        # Run
        result = await super().query(self.URL_API, query)

        # Check for Errors
        if raise_errors:
            self.raise_errors(result)

        return result.get("data", {}) # type: ignore

    async def multiquery(self, queries: list[str], raise_errors=True) -> list[typing.Any]:
        """Execute a list of queries as a batch.

        Args:
            queries(list[str]): the queries to run

        Returns:
            data[object]: the results in the same order

        """
        tasks = [self.query(query, raise_errors=raise_errors) for query in queries]
        return await asyncio.gather(*tasks) # type: ignore
