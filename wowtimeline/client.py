# -*- coding: utf-8 -*-
"""Warcaftlogs API Client"""

# IMPORT STANDARD LIBRARIES
import os
import json
from aiohttp import ClientSession
import aiofiles

import models



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
        async with aiofiles.open(self.filename, "w") as f:
            await f.write(json.dumps(self.data, indent=4, sort_keys=True))
        print("cache saved")


class WarcraftlogsClient:

    URL_API = "https://www.warcraftlogs.com/api/v2/client"
    URL_AUTH = "https://www.warcraftlogs.com/oauth/token"

    URL_APIv1 = "https://www.warcraftlogs.com:443/v1/"

    def __init__(self, client_id="", client_secret=""):
        super(WarcraftlogsClient, self).__init__()
        self.client_id = client_id or os.getenv("WCL_CLIENT_ID")
        self.client_secret = client_secret or os.getenv("WCL_CLIENT_SECRET")
        self.headers = {}

        self.cache = JsonCache()
        self.rate_limit_data = {}

    async def update_auth_token(self):
        """Request a new Auth Token from Warcraftlogs."""
        data = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }
        async with ClientSession() as session:
            async with session.post(url=self.URL_AUTH, data=data) as resp:
                data = await resp.json()

        token = data.get("access_token", "")
        self.headers["Authorization"] = "Bearer " + token

    async def query(self, query, usecache=True):

        # caching
        if usecache:
            await self.cache.load()
            cached_result = self.cache.data.get(query)
            if cached_result:
                print("using cached result")
                return cached_result

        # auth
        if not self.headers:
            await self.update_auth_token()

        async with ClientSession() as session:
            async with session.get(url=self.URL_API, json={"query": query}, headers=self.headers) as resp:

                try:
                    result = await resp.json()
                except Exception as e:
                    print(resp)
                    raise(e)

                # some reports are private.. but still show up in rankings..
                # lets just see what happens
                """
                if result.get("errors"):
                    msg = ""
                    for error in result.get("errors"):
                        msg += "\n" + error.get("message") + " path:" + "/".join(error.get("path"))
                        print(query)
                    raise ValueError(msg)
                """
                data = result.get("data", {})

                if usecache:
                    self.cache[query] = data

                return data

    async def _update_rate_limit_data(self):
        query = """
        {
            rateLimitData {
                pointsSpentThisHour
                limitPerHour
                pointsResetIn
            }
        }
        """
        result = await self.query(query, usecache=False)
        info = result.get("rateLimitData", {})
        info["points_left"] = info.get("limitPerHour", 0) - info.get("pointsSpentThisHour", 0)
        self.rate_limit_data = info

    async def get_points_left(self):
        await self._update_rate_limit_data()
        return self.rate_limit_data.get("points_left", 0)


    ##############################

    async def load_report(self, report_id):
        report = Report(report_id)
        report.client = self
        await report.fetch()
        return report

    async def load_fight(self, report_id, fight_id):
        fight = Fight(report_id, fight_id)
        fight.client = self
        await fight.fetch()
        return fight

    async def fetch_multiple_fights(self, fights):

        #############
        # Query
        query = ""
        for i, fight in enumerate(fights):
            query += f"report{i}: {fight.get_casts_query()}"

        query = f"""
        {{
            reportData
            {{
                {query}
            }}
        }}
        """
        data = await self.query(query)
        data = data.get("reportData", {})

        #############
        # process data
        for i, fight in enumerate(fights):
            report_data = data.get(f"report{i}", {})

            # skip if smth went wrong with this report
            if not report_data:
                continue

            player = fight.players[0] # fixme
            casts_data = report_data.get("casts", {}).get("data", {})
            for cast_data in casts_data:

                # skip additional events like "begincast"
                if cast_data["type"] != "cast":
                    continue

                cast = models.Cast(**cast_data)
                cast.spell = player.spec.all_spells.get(cast.spell_id) or models.DUMMY_SPELL  # fixme
                cast.fight = fight
                player.casts.append(cast)

        return fights

    async def get_top_ranks(self, encounter, spec, metric="", difficulty=5):
        """Get Top Ranks for a given encounter and spec."""
        metric = metric or spec.metric # use given metric. otherwise use spec default
        query = f"""
        {{
            worldData
            {{
                encounter(id: {encounter})
                {{
                    characterRankings(
                        className: "{spec.class_.name}",
                        specName: "{spec.name_slug_cap}",
                        metric: {metric},
                        includeCombatantInfo: false,
                    )
                }}
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

            player = models.Player(
                name=player_name,
                spec=spec,
                total=ranking_data.get("amount", 0)
            )
            fight.players = [player]
            fights.append(fight)
        return fights


if __name__ == '__main__':
    import asyncio
    asyncio.run(test())