"""Models to store our list of full reports.."""
from __future__ import annotations

import textwrap

# IMPORT STANDARD LIBRARIES
import typing
from datetime import datetime

# IMPORT LOCAL LIBRARIES
from lorgs import utils
from lorgs.clients import wcl
from lorgs.models import base, warcraftlogs_base, warcraftlogs_report
from lorgs.models.raid_boss import RaidBoss
from lorgs.models.warcraftlogs_fight import Fight
from lorgs.models.warcraftlogs_report import Report
from lorgs.models.wow_spec import WowSpec
from lorgs.models.wow_spell import WowSpell


class CompRankingFight(Fight):
    """A single Fight showing in the Comp Rankings"""

    # Config
    pkey: typing.ClassVar[str] = "{report_id}.{fight_id}"
    skey: typing.ClassVar[str] = "overview"


class CompRanking(base.DynamoDBModel, warcraftlogs_base.wclclient_mixin):
    """A Group/List of reports for a given Boss."""

    boss_slug: str
    # the nameslug of the boss

    # datetime: timetamp of last update
    updated: datetime = datetime.min

    reports: list[Report] = []
    """all reports for this boss."""

    # Config
    pkey: typing.ClassVar[str] = "{boss_slug}"
    skey: typing.ClassVar[str] = "overview"

    ##########################
    # Attributes
    #
    @property
    def valid(self):
        if not self.boss:
            return False
        return True

    @property
    def boss(self) -> RaidBoss:
        return RaidBoss.get(full_name_slug=self.boss_slug)

    ##########################
    # Methods
    #
    def get_reports(self, search: dict | None = None, limit: int = 50) -> list[Report]:
        """list: reports for this group."""

        filter_kwargs = {}

        # filter by boss
        filter_kwargs["report__fights__0__boss__boss_id"] = self.boss.id

        # filter by inputs
        search = search or {}
        # build the search arguments
        for key, value in search.items():
            prefix = f"report.{key}"
            search_kwargs = warcraftlogs_base.query_args_to_mongo(*value, prefix=prefix)
            filter_kwargs.update(search_kwargs)

        # Query
        reports = (
            CompRankingReport.objects
        )  # todo: find a way to use the self.reports list field instead
        reports = reports.filter(**filter_kwargs)
        reports = reports.order_by(
            "+report__fights__deaths", "+report__fights__duration"
        )
        reports = reports[:limit] if limit else reports
        return reports

    ############################################################################
    # Query
    #
    def _get_healing_cooldowns(self) -> str:  # typing.List[WowSpell]:
        """All Spells that are considered Healing-Cooldowns.

        Right now, this simply returns every spell healers have

        TODO:
            share logic with <BaseActor> ?

        """

        def join(*parts: str):
            return " and ".join(parts)

        queries: typing.List[str] = []
        healers: typing.List[WowSpec] = [
            spec for spec in WowSpec.all if spec.role.code == "heal"
        ]

        # Casts
        casts: typing.List[WowSpell] = utils.flatten(
            spec.all_spells for spec in healers
        )
        casts = [cast for cast in casts if cast.is_healing_cooldown()]
        if casts:
            cast_ids = WowSpell.spell_ids_str(casts)
            buffs_q = join(
                "source.role='healer'", "type='cast'", f"ability.id in ({cast_ids})"
            )
            queries.append(buffs_q)

        # Buffs
        buffs: typing.List[WowSpell] = utils.flatten(spec.all_buffs for spec in healers)
        buffs = [buff for buff in buffs if buff.is_healing_cooldown()]
        if buffs:
            buffs_ids = WowSpell.spell_ids_str(buffs)
            buffs_q = join(
                "target.role='healer'",
                "type in ('applybuff', 'removebuff')",
                f"ability.id in ({buffs_ids})",
            )
            queries.append(buffs_q)

        return self.combine_queries(*queries)

    @staticmethod
    def _get_raid_cds() -> typing.List[WowSpell]:
        """All spells of type RAID_CD.

        eg.: Darkness, RallyCry, AMZ
        """
        spells = [
            spell for spell in WowSpell.all if spell.spell_type == spell.TYPE_RAID
        ]
        return utils.uniqify(spells, key=lambda spell: spell.spell_id)

    @staticmethod
    def _get_raid_buffs() -> typing.List[WowSpell]:
        """All spells of type RAID_CD.

        eg.: Darkness, RallyCry, AMZ
        """
        spells = [
            spell for spell in WowSpell.all if spell.spell_type == spell.TYPE_BUFFS
        ]
        return utils.uniqify(spells, key=lambda spell: spell.spell_id)

    def get_filter(self) -> str:
        """Filter that is applied to the query."""
        filter_healing_cds = self._get_healing_cooldowns()

        raid_cds = self._get_raid_cds()
        raid_cds_str = WowSpell.spell_ids_str(raid_cds)
        raid_cds_filter = f"type='cast' and ability.id in ({raid_cds_str})"

        raid_buffs = self._get_raid_buffs()
        raid_buffs_str = WowSpell.spell_ids_str(raid_buffs)
        raid_buffs_filter = (
            f"type in ('applybuff', 'removebuff') and ability.id in ({raid_buffs_str})"
        )

        return self.combine_queries(
            filter_healing_cds, raid_cds_filter, raid_buffs_filter
        )

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

    ############################################################################
    # Query
    #

    def add_report(self, fight_data: wcl.FightRankingsFight):
        # print("Adding", fight_data)

        fight = CompRankingFight(
            fight_id=fight_data.report.fightID,
            start_time=fight_data.startTime,
            duration=fight_data.duration,
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
            # print("query_result", query_result)

            # parse data
            world_data = wcl.WorldData(**query_result)
            rankings = world_data.encounter.fightRankings
            load_more = rankings.hasMorePages

            # add fights
            for fight_data in rankings.rankings:

                # check if already in the list
                key = (fight_data.report.code, fight_data.report.fightID)
                if key in old_reports:
                    continue
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

    async def load(self, limit: int = 50, clear_old: bool = False):
        """Fetch reports for this BossRanking.

        params:
            limit (int): maximum number of reports to load.
            clear_old (bool): if true old reports will be deleted.

        """
        # old reports
        if clear_old:
            self.reports = []

        # new reports
        new_reports = await self.load_new_reports(limit=limit)

        return

        # compare old vs new reports
        old_report_keys = [report.key for report in self.reports]
        new_reports = [
            report for report in new_reports if report.key not in old_report_keys
        ]

        # load only the fights that need to be loaded
        fights = [report.fight for report in new_reports]
        fights = [fight for fight in fights if not fight.players]
        fights = fights[
            :limit
        ]  # should already be enforced from the "load_new_reports"... but better safe then sorry

        try:
            await self.load_many(fights)
        except PermissionError:
            pass  # private report

        for fight in fights:
            try:
                await self.load_fight(fight)
            except PermissionError:
                pass  # private report

        self.reports += new_reports
