"""Models to store our list of full reports.."""
from __future__ import annotations

# IMPORT STANDARD LIBRARIES
import textwrap
import typing
from datetime import datetime

# IMPORT LOCAL LIBRARIES
from lorgs.clients import wcl
from lorgs.logger import logger
from lorgs.models import base, warcraftlogs_base
from lorgs.models.raid_boss import RaidBoss
from lorgs.models.warcraftlogs_boss import Boss
from lorgs.models.warcraftlogs_fight import Fight
from lorgs.models.warcraftlogs_report import Report
from lorgs.models.wow_spell import SpellTag, WowSpell, build_spell_query


class CompRankingFight(Fight):
    """A single Fight showing in the Comp Rankings"""

    def get_query_parts(self) -> list[str]:

        spells = [spell for spell in WowSpell.list() if SpellTag.RAID_CD in spell.tags]
        filter_expr = build_spell_query(spells)
        query = f'events({self.table_query_args}, filterExpression: "{filter_expr}") {{data}}'

        parts = super().get_query_parts()
        parts.append(query)
        return parts

    async def load(self, *args, **kwargs):
        await super().load(*args, **kwargs)
        if self.boss:
            await self.boss.load(*args, **kwargs)


class CompRanking(base.S3Model, warcraftlogs_base.wclclient_mixin):
    """A Group/List of reports for a given Boss."""

    boss_slug: str
    # the nameslug of the boss

    # datetime: timetamp of last update
    updated: datetime = datetime.min

    reports: list[Report] = []
    """all reports for this boss."""

    # Config
    key: typing.ClassVar[str] = "{boss_slug}"

    @property
    def boss(self) -> RaidBoss | None:
        return RaidBoss.get(full_name_slug=self.boss_slug)

    ############################################################################
    # Query
    #
    def get_query(self, metric: str = "execution", page: int = 1) -> str:
        """Get the Query to load this Fight Rankings."""
        if not self.boss:
            raise ValueError(f"Unknown Boss: {self.boss_slug}")

        return textwrap.dedent(
            f"""
            worldData
            {{
                encounter(id: {self.boss.id})
                {{
                    fightRankings(
                        metric: {metric}
                        page: {page}
                    )
                }}
            }}
            """
        )

    def add_report(self, fight_data: wcl.FightRankingsFight):
        """Add a new Report/Fight to the Ranking."""
        boss = Boss(boss_slug=self.boss_slug)

        fight = CompRankingFight(
            fight_id=fight_data.report.fightID,
            start_time=fight_data.startTime,
            duration=fight_data.duration,
            boss=boss,
            players=[],
        )

        report = Report(
            report_id=fight_data.report.code,
            start_time=fight_data.report.startTime,
            fights=[fight],
        )

        self.reports.append(report)

    async def load_new_reports(self, metric: str = "execution", limit=50) -> list[Report]:
        """Get Top Fights for a given encounter."""
        limit = limit or 50  # in case limit defaults to 0 somewhere

        # build a list of old Reports
        old_reports: list[tuple[str, int]] = []
        for report in self.reports:
            for fight in report.fights:
                old_reports.append((report.report_id, fight.fight_id))

        new_reports: list[Report] = []
        load_more = True
        page = 0
        while load_more:  # nobody likes while loops
            page += 1

            # execute the query
            query = self.get_query(metric=metric, page=page)
            query_result = await self.client.query(query)
            query_result = query_result["worldData"]

            # parse data
            world_data = wcl.WorldData(**query_result)
            rankings = world_data.encounter.fightRankings
            load_more = rankings.hasMorePages

            # add fights
            for fight_data in rankings.rankings:
                key = (fight_data.report.code, fight_data.report.fightID)
                if key not in old_reports:
                    self.add_report(fight_data)

            # stop if limit is reached
            if len(self.reports) >= limit:
                load_more = False
                break

        self.reports = self.reports[:limit]
        return new_reports

    async def load_fight(self, fight: Fight):

        query = f"""
            reportData
            {{
                report(code: "{fight.report.report_id}")
                {{
                    events(
                        {fight.table_query_args},
                        filterExpression: "{self.get_filter()}"
                    )
                    {{data}}
                }}
            }}
        """
        query_result = await self.client.query(query=query)
        for actor in fight.players.values():
            actor.process_query_result(query_result)

        await fight.boss.load()

        fight.players = {
            k: player for k, player in fight.players.items() if player.has_own_casts
        }

    async def load(self, limit: int = 5, clear_old: bool = False):
        """Fetch reports for this BossRanking.

        params:
            limit (int): maximum number of reports to load.
            clear_old (bool): if true old reports will be deleted.

        """
        # old reports
        if clear_old:
            self.reports = []
        await self.load_new_reports(limit=limit)

        # 1) Load Fights
        fights_to_load = []
        for report in self.reports:
            for fight in report.fights:
                if not fight.players:
                    fights_to_load.append(fight)

        logger.info(f"Load {len(fights_to_load)} Fights")
        await self.load_many(fights_to_load, raise_errors=False)  # type: ignore

        self.updated = datetime.utcnow()
