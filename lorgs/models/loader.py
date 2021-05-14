"""Some Functions to load and create Models.

This could probl be added to either the Models or the Client Class..
but in order to keep them a bit more organized..
I decided to move all this logic to its own place

"""

# IMPORT STANDARD LIBRARIES
import asyncio

# IMPORT THIRD PARTY LIBRARIES
import textwrap

# IMPORT LOCAL LIBRARIES
from lorgs import utils
from lorgs.client import WarcraftlogsClient
from lorgs import db
from lorgs.logger import logger
from lorgs.models import warcraftlogs_ranking
from lorgs.models.encounters import RaidBoss
from lorgs.models.encounters import RaidZone
from lorgs.models.specs import WowClass
from lorgs.models.specs import WowSpec
from lorgs.models.specs import WowSpec
from lorgs.models.specs import WowSpell
# from lorgs.models.warcraftlogs import Cast
# from lorgs.models.warcraftlogs import Fight
# from lorgs.models.warcraftlogs import Player
# from lorgs.models.warcraftlogs import Report

# from lorgs.data import SPELLS


WCL_CLIENT = WarcraftlogsClient.get_instance()


################################################################################
#
#   CASTS
#
################################################################################



################################################################################
#
#   PLAYERS
#
################################################################################

################################################################################
#
#   FIGHTS
#
################################################################################




async def load_fights(fights):
    """Load a list of Fights.

    Args:
        fights[list(<Fight>)]

    """
    logger.debug("start loading %d fights", len(fights))
    queries = [fight_data_query(fight) for fight in fights]

    # Get Queries
    data = await WCL_CLIENT.multiquery(queries)

    # Process
    for fight, fight_data in zip(fights, data):
        report_data = fight_data.get("report") or {}
        players_data = report_data.get("players", {}).get("data", {})
        casts_data = report_data.get("casts", {}).get("data", [])

        for player in fight.players:
            player.casts = load_player_casts(player, casts_data)

    logger.debug("load_fights end")



################################################################################
#
#   RANKINGS
#
################################################################################

def fight_data_query2(fight, spells=None):
    """Construct the Query to fetch all info in a Fight.

    Args:
        fight(<Fight>): the fight we want to fetch
        spells[list(Spell)]: the spells we want to fetch (queries all spells if None)

    Returns:
        str: the constructed query string

    """

    def spell_ids(spells):
        spells = sorted(spell.spell_id for spell in spells)
        return ",".join(str(i) for i in spells)

    table_query_args = f"fightIDs: {fight.fight_id}, startTime: {fight.start_time}, endTime: {fight.end_time}"

    # Build Players Query (if needed)
    if fight.players:
        player_query = ""

        # Build Casts Filter
        casts_filters = [
            f"(source.name='{player.name}' and ability.id in ({spell_ids(player.spec.spells)}))"
            for player in fight.players
        ]
        casts_filter = " or ".join(casts_filters)

    else: # no player --> we need to fetch them
        all_spells = WowSpell.query.all()
        player_query = f"players: table({table_query_args}, dataType: Summary)"
        casts_filter = f"ability.id in ({spell_ids(spells or all_spells)})"

    logger.debug("player_query: %s", player_query)
    logger.debug("casts_filter: %s", casts_filter)

    casts_query = f"casts: events({table_query_args}, dataType: Casts, filterExpression: \"{casts_filter}\") {{data}}"
    return textwrap.dedent(f"""\
    reportData {{
        report(code: "{fight.report.report_id}") {{
            {player_query}
            {casts_query}
        }}
    }}
    """)



async def load_ranking_casts(players):
    """Load a list of Fights.

    Args:
        fights[list(<Fight>)]

    """
    logger.debug("start loading %d players", len(players))

    # Get Queries
    queries = [player._get_casts_query() for player in players]
    data = await WCL_CLIENT.multiquery(queries)

    # Process
    for player, fight_data in zip(players, data):
        report_data = fight_data.get("report") or {}
        casts_data = report_data.get("casts", {}).get("data", [])
        player._process_casts_data(casts_data)

    logger.debug("load_fights end")

async def load_char_rankings_source_ids(rankings):
    """Fetch and add the source_id's for ranking data."""
    queries = []
    for ranking_data in rankings:
        report_data = ranking_data.get("report", {})
        report_id = report_data.get("code")
        player_class = ranking_data.get("class")
        query = f"""\
            reportData
            {{
                report(code: "{report_id}")
                {{
                    masterData
                    {{
                        actors(type: "Player", subType: "{player_class}")
                        {{
                            name
                            id
                        }}
                    }}
                }}
            }}
            """
        queries.append(query)

    # run the queries
    data = await WCL_CLIENT.multiquery(queries)

    # process the data
    for ranking_data, report_data in zip(rankings, data):
        report_data = report_data.get("report") or {}
        master_data = report_data.get("masterData") or {}
        if not master_data:
            continue

        for actor in master_data.get("actors") or []:
            actor_name = actor.get("name")
            if actor_name == ranking_data["name"]:
                ranking_data["source_id"] = actor.get("id", -1)
                break


async def load_spec_rankings(boss, spec, difficulty=5, limit=50):
    """Get Top Ranks for a given boss and spec."""
    logger.info(f"{boss.name} vs. {spec.name} {spec.wow_class.name} START")

    # Build and run the query
    query = f"""\
    worldData
    {{
        encounter(id: {boss.id})
        {{
            characterRankings(
                className: "{spec.wow_class.name_slug_cap}",
                specName: "{spec.name_slug_cap}",
                metric: {spec.role.metric},
                includeCombatantInfo: false,
                serverRegion: "EU",
            )
        }}
    }}
    """

    data = await WCL_CLIENT.query(query)
    data = data.get("worldData", {}).get("encounter", {}).get("characterRankings", {})

    rankings = data.get("rankings", [])
    if limit:
        rankings = rankings[:limit]

    # not even needed? because we filter by name
    # logger.debug(f"{boss.name} vs. {spec.name} {spec.wow_class.name} load source ids")
    # await load_char_rankings_source_ids(rankings)

    players = []
    for ranking_data in rankings:
        report_data = ranking_data.get("report", {})

        # skip hidden reports
        if ranking_data.get("hidden"):
            continue


        ranked_char = warcraftlogs_ranking.RankedCharacter()
        ranked_char.spec = spec
        ranked_char.spec_id = spec.id
        ranked_char.boss_id = boss.id
        ranked_char.fight_id = report_data.get("fightID")
        ranked_char.player_name = ranking_data.get("name")
        ranked_char.amount = ranking_data.get("amount", 0)
        ranked_char.report_id = report_data.get("code")
        ranked_char.fight_time_start = ranking_data.get("startTime", 0) - report_data.get("startTime", 0)
        ranked_char.fight_time_end = ranked_char.fight_time_start + ranking_data.get("duration", 0)
        # db.session.add(ranked_char)
        players.append(ranked_char)

        """
        # Report
        report = Report(report_id=report_data.get("code"))

        # Fight
        fight = report.add_fight()
        fight.boss = boss
        fight.start_time = ranking_data.get("startTime", 0) - report_data.get("startTime", 0)
        fight.end_time = fight.start_time + ranking_data.get("duration", 0) # TODO: check property thing

        # Player
        player = fight.add_player()
        player.source_id = ranking_data.get("source_id")
        player.name = ranking_data.get("name")
        player.spec = spec
        player.total = ranking_data.get("amount", 0)
        """
        # reports.append(report)
        # players.append(player)

    ########################
    # load casts
    #
    logger.info(f"{boss.name} vs. {spec.name} {spec.wow_class.name} load casts")
    for i, chunk in enumerate(utils.chunks(players, 50)): # load in chunks of 10 each
        logger.info(f"{boss.name} vs. {spec.name} {spec.wow_class.name} load casts | chunk {i}")
        await load_ranking_casts(chunk)

    return players
