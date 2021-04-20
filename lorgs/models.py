
# IMPORT THIRD PARTY LIBRARIES
import textwrap

# IMPORT LOCAL LIBRARIES
from lorgs import utils
from lorgs.logger import logger

###############################
# Constant Data


class WoWSpell:
    """Container to define a spell."""

    _all = {}

    # def __new__(cls, spell_id, *args, **kwargs):
    #     """Create a new spell or reuse an instance if we already have that spell."""
    #     if spell_id not in cls._all:
    #         instance = super(WoWSpell, cls).__new__(cls)
    #         cls._all[spell_id] = instance
    #     return cls._all[spell_id]

    def __init__(self, spell_id, duration=0, cooldown=0, show=True, group=None):
        super().__init__()

        # game info
        self.spell_id = spell_id
        self.duration = duration
        self.cooldown = cooldown

        # display info
        self.group = group
        self.show = show

    def __repr__(self):
        return f"<Spell({self.spell_id}, cd={self.cooldown})>"

    def __eq__(self, other):
        return self.spell_id == other.spell_id

    def __hash__(self):
        key = (self.spell_id, self.duration, self.cooldown, self.group)
        return hash(key)


DUMMY_SPELL = WoWSpell(spell_id=0)


class WowSpec:
    """docstring for Spec"""

    def __init__(self, class_, name, role="dps"):
        super().__init__()
        self.id = 0
        self.name = name
        self.role = role
        self.class_ = class_
        self.spells = {}

        # used for sorting
        role_order = {"tank": 0, "heal": 1, "rdps": 2, "mdps": 3, "other": 4}
        self.role_index = role_order.get(self.role, 99)

        # bool: is this spec is currently supported
        self.supported = True

        # Generate some names
        self.class_name = self.class_.name
        self.full_name = f"{self.name} {self.class_name}"
        self.short_name = self.name # to be overwritten

        # slugified names
        self.name_slug = utils.slug(self.name)
        self.class_name_slug = self.class_.name_slug
        self.full_name_slug = f"{self.class_name_slug}-{self.name_slug}"

        # str: Spec Name without spaces, but still capCase.. eg.: "BeastMastery"
        self.name_slug_cap = self.name.replace(" ", "")

    def __repr__(self):
        return f"<Spec({self.full_name})>"

    @property
    def _sort_tuple(self):
        return (self.role_index, self.name, self.full_name_slug)

    def __lt__(self, other):
        return self._sort_tuple < other._sort_tuple

    def add_spell(self, **kwargs):
        kwargs["group"] = kwargs.get("group") or self
        spell = WoWSpell(**kwargs)
        self.spells[spell.spell_id] = spell
        return spell

    @property
    def all_spells(self):
        return self.spells
        # return {**self.spells, **self.class_.spells}

    @property
    def metric(self):
        """str: the preferred metric. aka: dps for all. hps for healers"""
        if self.role == "heal":
            return "hps"
        return "dps"


class WoWClass:
    """docstring for WoWClass"""

    _all = {}

    def __init__(self, name):
        super().__init__()
        self.name = name
        self.specs = []
        self.id = 0
        self._all[self.name_slug] = self

    def __repr__(self):
        return f"<Class(name='{self.name}')>"

    def add_spell(self, *args, **kwargs):
        for spec in self.specs:
            spec.add_spell(*args, **kwargs)

    @classmethod
    def get_by_name(cls, name):
        name = utils.slug(name)
        return cls._all.get(name)

    @property
    def name_slug_cap(self):
        return self.name.replace(" ", "")

    @property
    def name_slug(self):
        return utils.slug(self.name)

    def add_spec(self, **kwargs):
        spec = WowSpec(self, **kwargs)
        # spec.class_ = self
        self.specs.append(spec)
        return spec

    def get_spec(self, name):
        name = utils.slug(name)
        specs = {s.name_slug: s for s in self.specs}
        return specs.get(name)


###############################
# Log/Fight Based


class Cast:
    """docstring for Cast"""
    def __init__(self, **kwargs):
        super(Cast, self).__init__()
        self.timestamp = kwargs.get("timestamp")
        self.spell_id = kwargs.get("abilityGameID")
        self.sourceid = kwargs.get("sourceID")

        self.player = None
        self.fight = None
        self.spell = None # WowSpell

    def __repr__(self):
        return f"Cast({self.spell_id}, at={self.time_fmt})"

    @property
    def time(self):
        return self.timestamp - self.fight.start_time

    @property
    def time_fmt(self):
        return utils.format_time(self.time)


class Player:
    """docstring for Player"""
    def __init__(self, name="", spec=None, total=0):
        super(Player, self).__init__()
        self.name = name
        self.spec = spec # WowSpec
        self.total = total
        self.casts = []

        self.fight = None # <Fight>
        self.source_id = 0  # the in the report/fight

    def __repr__(self):
        return f"Player({self.name}, spec={self.spec.name} id={self.source_id} casts={len(self.casts)})"

    @property
    def total_fmt(self):
        return utils.format_big_number(self.total)

    @property
    def report_url(self):
        return f"{self.fight.report_url}&source={self.source_id}"

    @property
    def spells_used(self):
        spells = [cast.spell for cast in self.casts]
        return list(set(spells))



class Fight:
    """Basically a pull"""
    def __init__(self, report_id, fight_id, **kwargs):
        super(Fight, self).__init__()
        self.client = None
        self.report = Report(report_id)
        self.report_id = report_id
        self.fight_id = fight_id

        self.data = {}
        self.start_time = kwargs.get("start_time", 0)
        self.end_time = kwargs.get("end_time", 999999999999)
        self.encounter_id = -1
        # self.fightPercentage = args.get("fightPercentage")
        # self.kill = args.get("kill")

        self.players = []
        self.casts = []

        # str: extra filter for the query
        self.filter_expression = kwargs.get("filter_expression", "")

        self.query_name = f"fight_{self.report_id}_{self.fight_id}"

    def __repr__(self):
        return f"Fight({self.report_id}, {self.fight_id})"

    @property
    def duration(self):
        return self.end_time - self.start_time

    @property
    def duration_fmt(self):
        return utils.format_time(self.duration)

    @property
    def report_url(self):
        return f"{self.report.report_url}#fight={self.fight_id}"

    def get_casts_query(self):

        return textwrap.dedent(
            f"""report(code: "{self.report_id}")
                {{
                    casts: events(
                        fightIDs: {self.fight_id}, startTime: {self.start_time}, endTime: {self.end_time},
                        dataType: Casts,
                        filterExpression: "{self.filter_expression}"
                    ) {{data}}
                }}
            """)
        """
        """

    async def fetch_fight_data(self):
        pass
        '''
        query = f"""
        {{
            reportData {{
                report(code: "{self.report_id}") {{
                    fights(fightIDs: {self.fight_id}) {{
                        id
                        encounterID
                        fightPercentage
                        kill
                        startTime
                        endTime
                    }}
                }}
            }}
        }}
        """
        self.data = await self.client.query(query)
        data_fight = self.data.get("reportData", {}).get("report", {}).get("fights", [])[-1]

        self.startTime = data_fight.get("startTime") or self.startTime
        self.endTime = data_fight.get("endTime") or self.endTime
        self.encounterID = data_fight.get("encounterID") or self.encounterID
        '''

    def _process_player_data(self, players_data):
        if not players_data:
            return

        # player_by_id = {}  # TODO: add to FightClass
        for composition_data in players_data.get("composition", []):
            player = Player()
            player.fight = self
            player.source_id = composition_data.get("id")
            player.name = composition_data.get("name")

            class_name = composition_data.get("type")
            wow_class = WoWClass.get_by_name(class_name)
            if not wow_class:
                logger.warning("Unknown Class: %s", class_name)
                continue

            spec_data = composition_data.get("specs", [])
            if not spec_data:
                logger.warning("Player has no spec: %s", player.name)
                continue

            spec_data = spec_data[0]
            spec_name = spec_data.get("spec")
            player.spec = wow_class.get_spec(spec_name)
            # self.players.append(player)
            if not player.spec:
                logger.warning("Unknown Spec: %s", spec_name)
                continue

            yield player

            # spec_role = spec_data.get("role")
            # if spec_role != "healer":
            #     continue
            # player.role = player_spec.get("role")
            # player_by_id[player.source_id] = player

        """
        # who asked?
        for damage_data in players_data.get("damageDone", []):
            player_id = damage_data.get("id", -1)
            player = self.players.get(player_id)
            if player:
                player.damage_done = damage_data.get("total", 0)

        for damage_data in players_data.get("healingDone", []):
            player_id = damage_data.get("id", -1)
            player = self.players.get(player_id)
            if player:
                player.healing_done = damage_data.get("total", 0)
        """

    def _build_query(self, spells=None, extra_filter=""):
        table_query_args = f"fightIDs: {self.fight_id}, startTime: {self.start_time}, endTime: {self.end_time}"

        # Build Casts Filter
        if self.players:
            casts_filters = []
            for player in self.players:
                spells = tuple(player.spec.all_spells.keys())
                casts_filter = f"(source.name='{player.name}' and ability.id in {spells})"
                casts_filters.append(casts_filter)
            casts_filter = " or ".join(casts_filters)

        else:
            spells = spells or (spell for spell in WoWSpell._all.keys() if spell > 0)
            spells = ",".join(str(s.spell_id) for s in spells)
            casts_filter = f"ability.id in ({spells})" if spells else ""

        if extra_filter:
            casts_filter = f"({casts_filter}) and ({extra_filter})"

        # see if we need to request player details
        # request_player_data = len(self.players) == 0
        # if request_player_data:
        #     pass
        # else:
        #     player_query = ""
        player_query = f"players: table({table_query_args}, dataType: Summary)"
        if len(self.players) == 1:
            # if its only 1 player, then our casts-filter should be enough to get all the info we need
            player_query = ""

        query = textwrap.dedent(f"""\
        reportData {{
            report(code: "{self.report_id}") {{
                {player_query}

                casts: events(
                    {table_query_args},
                    dataType: Casts,
                    filterExpression: "{casts_filter}"
                ) {{data}}
            }}
        }}
        """)
        return query

    def _process_query_data(self, data):

        report_data = data.get("report", {})
        report_data = report_data or data.get("reportData", {}).get("report", {})  # not sure which one is correct

        logger.debug(f"fetched fights: {self.report_id}")

        casts_data = report_data.get("casts", {}).get("data", {})
        casts_data = [c for c in casts_data if c.get("type") == "cast"] # skip additional events like "begincast"
        # TODO: at some point i should check for "begincast" instead.. for non instant casts

        ################
        # Players
        if len(self.players) == 1:
            player = self.players[0]
            for cast_data in casts_data:
                source_id = cast_data.get("sourceID")
                if source_id:
                    player.source_id = source_id
                    break

        elif self.players:
            # fill in data from query
            raise NotImplementedError

        else:
            # read player info's from query
            players_data = report_data.get("players", {}).get("data", {})
            players = self._process_player_data(players_data)
            self.players = list(players)

        ################
        # Casts
        ################
        player_by_id = {p.source_id: p for p in self.players}
        for cast_data in casts_data:
            cast = Cast(**cast_data)
            player = player_by_id.get(cast.sourceid)
            if not player:
                continue

            cast.spell = player.spec.spells.get(cast.spell_id)
            if not cast.spell:
                continue
            cast.fight = self
            player.casts.append(cast)

        # remove players with no casts
        self.players = [p for p in self.players if p.casts]

    async def fetch(self, client, spells=(), extra_filter=""):
        # we need to fetch the fight itself
        if self.start_time <= 0:
            await self.fetch_fight_data()

        query = self._build_query(spells=spells, extra_filter=extra_filter)
        data = await client.query(query)
        self._process_query_data(data)



class Report:
    """docstring for Fight"""
    def __init__(self, report_id):
        super().__init__()
        self.report_id = report_id
        self.guild = ""
        self.realm = ""
        self.region = ""

    @property
    def report_url(self):
        return f"https://www.warcraftlogs.com/reports/{self.report_id}"

    async def fetch_fights(self, client):
        """
        TODO: move to client and combine processing logic?
        """
        query = f"""
        reportData
        {{
            report(code: "{self.report_id}")
            {{
                fights
                {{
                    id
                    encounterID
                    fightPercentage
                    kill
                    startTime
                    endTime
                }}
            }}
        }}
        """

        data = await client.query(query)
        report_data = data.get("reportData", {}).get("report", {})

        fights = []
        for fight_data in report_data.get("fights", []):

            fight_start_time = fight_data.get("startTime", 0) - report_data.get("startTime", 0)
            fight_end_time = fight_data.get("endTime", 0)

            # build filter
            fight = Fight(
                report_id=self.report_id,
                fight_id=fight_data.get("id"),
                start_time=fight_start_time,
                end_time=fight_end_time,
            )
            fights.append(fight)
        return fights
