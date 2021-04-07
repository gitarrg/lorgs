

# IMPORT THIRD PARTY LIBRARIES
import textwrap

# IMPORT LOCAL LIBRARIES
from wowtimeline import utils


###############################
# Constant Data


class WoWSpell:
    """Container to define a spell."""
    _all = {}

    def __init__(self, spell_id, duration=0, cooldown=0):
        super().__init__()
        self.spell_id = spell_id
        self.duration = duration
        self.cooldown = cooldown

        self._all[spell_id] = self

    def __repr__(self):
        return f"<WoWSpell({self.spell_id}, cooldown={self.cooldown})>"


DUMMY_SPELL = WoWSpell(spell_id=0)


class spell_mixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.spells = {}

    def add_spell(self, spell_id, **kwargs):
        spell = WoWSpell(spell_id=spell_id, **kwargs)
        self.spells[spell_id] = spell
        return spell


class WowSpec(spell_mixin):
    """docstring for Spec"""
    _all = {}

    def __init__(self, spec_id, name, role="dps"):
        super().__init__()
        self.spec_id = spec_id
        self.name = name
        self.role = role
        self.class_ = None
        self._all[spec_id] = self

    def __repr__(self):
        return f"<WoWSpec({self.full_name})>"

    @property
    def full_name(self):
        return f"{self.name} {self.class_.name}"

    @property
    def name_slug(self):
        return self.full_name.replace(" ", "-").lower()

    @property
    def all_spells(self):
        return {**self.spells, **self.class_.spells}

    @property
    def metric(self):
        """str: the preferred metric. aka: dps for all. hps for healers"""
        if self.role == "heal":
            return "hps"
        return "dps"


class WoWClass(spell_mixin):
    """docstring for WoWClass"""
    _all = {}

    def __init__(self, class_id, name):
        super().__init__()
        self.class_id = class_id
        self.name = name
        self.specs = {}

        self._all[class_id] = self

    def __repr__(self):
        return f"<WoWClass(name='{self.name}')>"

    def add_spec(self, spec_id, **kwargs):
        spec = WowSpec(spec_id, **kwargs)
        spec.class_ = self
        self.specs[spec_id] = spec
        return spec


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
    def __init__(self, name="", spec=None):
        super(Player, self).__init__()
        self.id = 0
        self.name = name

        # self.type = ""  # aka class
        self.spec = spec # WowSpec

        self.damage_done = 0
        self.healing_done = 0

        self.casts = []

    @property
    def class_slug(self):
        return self.spec.class_.name.lower().replace(" ", "")  # fixme


class Fight:
    """Basically a pull"""
    def __init__(self, report_id, fight_id, **kwargs):
        super(Fight, self).__init__()
        self.client = None
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

    def __repr__(self):
        return f"Fight({self.report_id}, {self.fight_id})"

    @property
    def duration(self):
        return self.end_time - self.start_time

    @property
    def duration_fmt(self):
        return utils.format_time(self.duration)

    @property
    def url(self):
        return f"https://www.warcraftlogs.com/reports/{self.report_id}#fight={self.fight_id}"

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

    async def fetch(self, spells=()):

        # we need to fetch the fight itself
        if self.startTime <= 0:
            await self.fetch_fight_data()

        table_query_args = f"fightIDs: {self.fight_id}, startTime: {self.startTime}, endTime: {self.endTime}"
        spells = ",".join(str(s) for s in spells)
        query = f"""
        {{
            reportData {{
                report(code: "{self.report_id}") {{
                    players: table({table_query_args}, dataType: Summary)

                    casts: events(
                        {table_query_args},
                        dataType: Casts,
                        filterExpression: "ability.id in ({spells})"
                    ) {{data}}
                }}
            }}
        }}
        """
        self.data = await self.client.query(query)
        report_data = self.data.get("reportData", {}).get("report", {})

        ################
        # Players
        players_data = report_data.get("players", {}).get("data", {})

        for composition_data in players_data.get("composition", []):
            player = Player()
            player.id = composition_data.get("id")
            player.name = composition_data.get("name")
            player.type = composition_data.get("type")

            player_spec = composition_data.get("specs", [])[0]
            player.spec = player_spec.get("spec")
            player.role = player_spec.get("role")
            self.players[player.id] = player

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
        # for _, player in self.players.items():
        #     print(f"{player.name:15s} | {player.spec:12} | {player.damage_done:,.0f} | {player.healing_done:,.0f}")

        ################
        # Casts
        ################
        casts_data = report_data.get("casts", {}).get("data", {})

        for data in casts_data:
            cast = Cast(**data)
            cast.player = self.players.get(cast.sourceid)
            cast.fight = self
            self.casts.append(cast)
            cast.player.casts.append(cast)


class Report:
    """docstring for Fight"""
    def __init__(self, report_id):
        super().__init__()
        self.report_id = report_id
        self.client = None

        self.data = {}

        self.title = ""
        self.fights = []

    async def fetch(self):
        # format the query
        query = f"""
        {{
            reportData {{
                report(code: "{self.report_id}") {{
                    title
                    fights {{
                        id
                        startTime
                        endTime
                    }}
                }}
            }}
        }}
        """
        self.data = await self.client.query(query)

        # Unpack the data
        report_data = self.data.get("reportData", {}).get("report", {})
        self.title = report_data.get("title", "")

        for data in report_data.get("fights", []):
            data["report_id"] = self.report_id
            self.fights += [Fight(**data)]

        return self.data
