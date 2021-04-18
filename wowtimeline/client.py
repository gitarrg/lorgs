# -*- coding: utf-8 -*-
"""Warcaftlogs API Client"""

# IMPORT STANDARD LIBRARIES
import os
import json
import asyncio
import aiohttp
import aiofiles

# IMPORT LOCAL LIBRARIES
from wowtimeline import models
from wowtimeline.logger import logger


def with_semaphore(limit=25):
    sem = asyncio.Semaphore(limit)

    def decorator(func):
        async def wrapped(*args, **kwargs):
            async with sem:
                return await func(*args, **kwargs)
        return wrapped
    return decorator


class JsonCache:

    def __init__(self, filename="cache.json"):
        self.filename = filename
        self.data = {}

        self.get = self.data.get

    def __setitem__(self, key, item):
        self.data[key] = item

    def __getitem__(self, key):
        return self.data[key]

    def clear(self):
        self.data = {}

    async def load(self, force=False):

        if force:
            self.data = {}

        # we already have some data loaded
        if self.data:
            return

        if not os.path.isfile(self.filename):
            return self.data

        async with aiofiles.open(self.filename, "r") as f:
            content = await f.read()
            self.data = json.loads(content)
            return self.data

    async def save(self):
        if not self.data:
            logger.info(f"nothing to be saved..")
            return

        async with aiofiles.open(self.filename, "w") as f:
            await f.write(json.dumps(self.data, indent=4, sort_keys=True))
        logger.info(f"saved cache to disc: {self.filename}")


class WarcraftlogsClient:

    URL_API = "https://www.warcraftlogs.com/api/v2/client"
    URL_AUTH = "https://www.warcraftlogs.com/oauth/token"

    def __init__(self, client_id="", client_secret=""):
        super(WarcraftlogsClient, self).__init__()

        # credentials
        self.client_id = client_id or os.getenv("WCL_CLIENT_ID")
        self.client_secret = client_secret or os.getenv("WCL_CLIENT_SECRET")

        self.headers = {}

        self.cache = JsonCache()
        # self.connector = aiohttp.TCPConnector(limit_per_host=9999999)

    ##############################

    async def update_auth_token(self):
        """Request a new Auth Token from Warcraftlogs."""
        data = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(url=self.URL_AUTH, data=data) as resp:

                try:
                    data = await resp.json()
                except Exception as e:
                    logger.error(resp)
                    raise e

        token = data.get("access_token", "")
        self.headers["Authorization"] = "Bearer " + token

    # @with_semaphore(25)
    async def query(self, query, usecache=True):

        query = f"""
        query {{
            {query}
        }}"""

        # caching
        if usecache:
            cached_result = usecache and self.cache.data.get(query)
            if cached_result:
                logger.debug("using cached result")
                return cached_result

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
                if result.get("errors"):
                    msg = ""
                    for error in result.get("errors"):
                        msg += "\n" + error.get("message") + " path:" + "/".join(error.get("path", []))
                        print(query)
                    raise ValueError(msg)
                """
                """
                data = result.get("data", {})

                if usecache:
                    self.cache[query] = data

                return data

    async def get_points_left(self):
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

    ##############################

    async def fetch_classids(self, wow_classes):

        classes_by_name = {c.name: c for c in wow_classes}

        # Classes and Specs
        query = """
        {
            gameData
            {
                classes
                {
                    id
                    name
                    specs
                    {
                        id
                        name
                    }
                }
            }
        }
        """
        result = await self.query(query)
        for class_data in result.get("gameData", {}).get("classes", []):
            class_name = class_data.get("name")
            wow_class = classes_by_name.get(class_name)
            if wow_class:
                wow_class.id = class_data.get("id", -1)
                for spec_data in class_data.get("specs", []):
                    spec = wow_class.get_spec(spec_data.get("name"))
                    if spec:
                        spec.id = spec_data.get("id", -1)

    ##############################

    async def fetch_multiple_fights(self, fights, **kwargs):

        if not fights:  # might happen in debugging
            logger.warning("No fights passed")
            return

        # alias and combine all queries
        query = ""
        for i, fight in enumerate(fights):
            fight_name = f"report_{i}"
            fight_query = fight._build_query(**kwargs)
            query += f"\n{fight_name}: {fight_query}"

        # run
        data = await self.query(query)

        # split and process
        for i, fight in enumerate(fights):
            fight_name = f"report_{i}"
            fight_data = data.get(fight_name)
            fight._process_query_data(fight_data)

    async def get_top_ranks(self, encounter, spec, metric="", difficulty=5):
        """Get Top Ranks for a given encounter and spec."""
        metric = metric or spec.metric # use given metric. otherwise use spec default
        query = f"""\
        worldData
        {{
            encounter(id: {encounter})
            {{
                characterRankings(
                    className: "{spec.class_.name_slug_cap}",
                    specName: "{spec.name_slug_cap}",
                    metric: {metric},
                    includeCombatantInfo: false,
                    serverRegion: "EU",
                )
            }}
        }}
        """
        data = await self.query(query)
        data = data.get("worldData", {}).get("encounter", {}).get("characterRankings", {})
        rankings = data.get("rankings", [])

        spell_ids = ",".join(str(s) for s in spec.all_spells.keys())

        fights = []
        for ranking_data in rankings:
            report_data = ranking_data.get("report", {})

            # skip hidden reports
            if ranking_data.get("hidden"):
                continue

            # skip asian reports (sorry)
            # server_region = ranking_data.get("server", {}).get("region", "")
            # if server_region not in ("EU", "US"):
            #     continue

            fight_start_time = ranking_data.get("startTime", 0) - report_data.get("startTime", 0)
            fight_end_time = fight_start_time + ranking_data.get("duration", 0)

            # build filter
            player_name = ranking_data["name"]

            filter_expression = f"ability.id in ({spell_ids}) and source.name='{player_name}'"
            fight = models.Fight(
                report_id=report_data.get("code"),
                fight_id=report_data.get("fightID"),
                start_time=fight_start_time,
                end_time=fight_end_time,
                filter_expression=filter_expression
            )

            player = models.Player(name=player_name, spec=spec)
            player.total = ranking_data.get("amount", 0)
            player.fight = fight

            fight.players = [player]
            fights.append(fight)
        return fights

    async def find_reports(self, encounter, search="", metric="execution"):
        """Get Top Fights for a given encounter."""

        rankings = []

        for i in range(3):  # fixme
            query = f"""
            worldData
            {{
                encounter(id: {encounter})
                {{
                    fightRankings(
                        metric: {metric},
                        filter: "{search}",
                        page: {i+1}
                    )
                }}
            }}
            """
            data = await self.query(query)
            data = data.get("worldData", {}).get("encounter", {}).get("fightRankings", {})
            rankings += data.get("rankings", [])

        fights = []
        for ranking_data in rankings:
            report_data = ranking_data.get("report", {})

            # skip hidden reports
            if ranking_data.get("hidden"):
                continue

            # skip asian reports (sorry)
            # server_region = ranking_data.get("server", {}).get("region", "")
            # if server_region not in ("EU", "US"):
            #     continue

            fight_start_time = ranking_data.get("startTime", 0) - report_data.get("startTime", 0)
            fight_end_time = fight_start_time + ranking_data.get("duration", 0)

            # TODO: get FightSummary and load players dynamic
            # from wowtimeline import wow_data
            # spell_ids = [spell for wow_class in wow_data.HEALS for spell in wow_class.all_spells]
            # spell_ids = set(spell_ids)
            # filter_expression = f"ability.id in ({spell_ids})"

            fight = models.Fight(
                report_id=report_data.get("code"),
                fight_id=report_data.get("fightID"),
                start_time=fight_start_time,
                end_time=fight_end_time,
                # filter_expression=filter_expression
            )
            fight.report.guild = ranking_data.get("guild", {}).get("name", "")
            fight.report.realm = ranking_data.get("server", {}).get("name", "")
            fight.report.region = ranking_data.get("server", {}).get("region", "")

            # player = models.Player(name=player_name, spec=</a>spec)
            # player.total = ranking_data.get("amount", 0)
            # player.fight = fight

            # fight.players = [player]
            fights.append(fight)
        return fights




if __name__ == '__main__':
    import asyncio
    from wowtimeline.main import WCL_CLIENT

    # search = "2.4.1,6.1.1,7.1.1,9.3.1|abilities.316958"
    # asyncio.run(WCL_CLIENT.find_reports(encounter=2407, search=search))


