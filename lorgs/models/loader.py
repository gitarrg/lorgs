"""Some Functions to load and create Models.

This could probl be added to either the Models or the Client Class..
but in order to keep them a bit more organsied..
I decided to move all this logic to its own place

"""


# IMPORT THIRD PARTY LIBRARIES
import textwrap

# IMPORT LOCAL LIBRARIES
from lorgs.client import WarcraftlogsClient
from lorgs.logger import logger
from lorgs.models.reports import Report, Fight, Player, Cast
from lorgs.models.specs import WowRole, WowClass, WowSpec, WowSpell
from lorgs import utils


WCL_CLIENT = WarcraftlogsClient.get_instance()


################################################################################
#
#   CASTS
#
################################################################################

@utils.as_list
def load_player_casts(player, casts_data):
    """Process the result of a casts-query to create Cast objects."""
    if not casts_data:
        logger.warning("casts_data is empty")
        return

    for cast_data in casts_data:
        if cast_data.get("sourceID") != player.source_id:
            continue

        cast = Cast()
        cast.spell_id = cast_data["abilityGameID"]
        cast.timestamp = cast_data["timestamp"]
        # cast.report = self.report
        # cast.fight = self.fight
        yield cast


################################################################################
#
#   PLAYERS
#
################################################################################

@utils.as_list
def load_fight_players(fight, players_data):
    if not players_data:
        logger.warning("players_data is empty")
        return

    total_damage = players_data.get("damageDone", [])
    total_healing = players_data.get("healingDone", [])

    # player_by_id = {}  # TODO: add to FightClass
    for composition_data in players_data.get("composition", []):

        spec_data = composition_data.get("specs", [])
        if not spec_data:
            logger.warning("Player has no spec: %s", composition_data.get("name"))
            continue

        spec_data = spec_data[0]
        spec_name = spec_data.get("spec")
        class_name = composition_data.get("type")

        spec = WowSpec.query
        spec = spec.join(WowSpec.wow_class) # join the class so we can filter
        spec = spec.filter(WowClass.name == class_name)
        spec = spec.filter(WowSpec.name == spec_name)
        spec = spec.first()
        if not spec:
            logger.warning("Unknown Spec: %s", spec_name)
            continue

        # Get Total Damage or Healing
        spec_role = spec_data.get("role")
        total_data = total_healing if spec_role == "healer" else total_damage
        for data in total_data:
            if data.get("id", -1) == composition_data.get("id"):
                total = data.get("total", 0) / (fight.duration / 1000)
                break
        else:
            total = 0

        # create and return yield player object
        player = Player()
        player.spec = spec
        player.name = composition_data.get("name")
        player.total = total
        player.source_id = composition_data.get("id")
        yield player


################################################################################
#
#   FIGHTS
#
################################################################################

def fight_data_query(fight, spells=None):
    """Construct the Query to fetch all info in a Fight.

    Args:
        fight(<Fight>): the fight we want to fetch
        spells[list(Spell)]: the spells we want to fetch (queries all spells if None)

    Returns:
        str: the constructed query string

    """
    table_query_args = f"fightIDs: {fight.fight_id}, startTime: {fight.start_time}, endTime: {fight.end_time}"

    # Build Players Query (if needed)
    if not fight.players:
        player_query = f"players: table({table_query_args}, dataType: Summary)"
    else:
        player_query = ""

    # Build Casts Filter
    if fight.players:
        casts_filters = []
        for player in fight.players:
            spells = tuple(player.spec.all_spells.keys())
            casts_filter = f"(source.name='{player.name}' and ability.id in {spells})"
            casts_filters.append(casts_filter)
        casts_filter = " or ".join(casts_filters)

    else:
        spells = spells or WowSpell.query.all()
        spells = ",".join(str(s.spell_id) for s in spells)
        casts_filter = f"ability.id in ({spells})" if spells else ""

    # if extra_filter:
    #     casts_filter = f"({casts_filter}) and ({extra_filter})"

    # see if we need to request player details
    # request_player_data = len(self.players) == 0
    # if request_player_data:
    #     pass
    # else:
    #     player_query = ""

    casts_query = f"casts: events({table_query_args}, dataType: Casts, filterExpression: \"{casts_filter}\") {{data}}"

    query = textwrap.dedent(f"""\
    reportData {{
        report(code: "{fight.report.report_id}") {{
            {player_query}
            {casts_query}
        }}
    }}
    """)
    return query


async def load_fights(fights):
    """Load a list of Fights.

    Args:
        fights[list(<Fight>)]

    """
    queries = [fight_data_query(fight) for fight in fights]
    data = await WCL_CLIENT.multiquery(queries)

    for fight, fight_data in zip(fights, data):

        report_data = fight_data.get("report", {})
        players_data = report_data.get("players", {}).get("data", {})
        casts_data = report_data.get("casts", {}).get("data", [])

        fight.players = load_fight_players(fight, players_data)

        for player in fight.players:
            player.casts = load_player_casts(player, casts_data)

        # load_fight_casts()


    return


################################################################################
#
#   REPORTS
#
################################################################################

async def load_report_info(report, fight_ids=None):
    """Fetch all fights in this report.

    Args:
        report(<Report>): the report

        fight_ids(list[int], optional): list of fights to load.
            loads all fights, if not specified.

    """
    query = f"""
    reportData
    {{
        report(code: "{report.report_id}")
        {{
            title
            zone {{name id}}
            startTime

            # masterData
            # {{
            #     actors(type: "Player")
            #     {{
            #         name
            #         id
            #     }}
            # }}

            fights(fightIDs: {fight_ids or []})
            {{
                id
                encounterID
                startTime
                endTime
                fightPercentage
                # kill
            }}
        }}
    }}
    """
    data = await WCL_CLIENT.query(query)
    report_data = data.get("reportData", {}).get("report", {})

    # Update the Report itself
    report.title = report_data.get("title", "")
    report.start_time = report_data.get("startTime", 0)
    report.zone_id = report_data.get("zone", {}).get("id", -1)

    # Update the Fights in this report
    for fight_data in report_data.get("fights", []):

        boss_id = fight_data.get("encounterID")
        if not boss_id:
            continue

        # Get the fight
        fight = Fight.get_or_create(report=report, fight_id=fight_data.get("id"))
        fight.start_time = fight_data.get("startTime", 0)
        fight.end_time = fight_data.get("endTime", 0)
        fight.boss_id = boss_id
        fight.percent = fight_data.get("fightPercentage")
        # kill = fight_data.get("kill")

        # fight.boss = encounter

        # fight = models.Fight.get(report=self, fight_id=fight_data.get("id"))
        # fight.start_time = fight_data.get("startTime", 0) - report.start_time
        # fight.end_time = fight_data.get("endTime", 0) - report.start_time
        report.fights.append(fight)


async def load_report(report):
    """Load a single Report.

    Args:
        report(<Report>): the report to load.

    """
    logger.info(f"{report} | start")
    if not report.fights:
        logger.info(f"{report} | load info")
        await load_report_info(report)

    # fights = report.fights[:3]

    fights_to_load = [fight for fight in report.fights if not fight.players]
    await load_fights(fights_to_load)

    return report
