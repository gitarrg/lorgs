"""Models for Warcraftlog-Reports/Fights/Actors."""

# pylint: disable=too-few-public-methods

# IMPORT THIRD PARTY LIBRARIES
import sqlalchemy
from sqlalchemy.ext.associationproxy import association_proxy


# IMPORT LOCAL LIBRARIES
from lorgs import utils
from lorgs.db import db
from lorgs.logger import logger

from lorgs.models.specs import WowClass, WowSpec, WowSpell


class Report(db.Model):
    """docstring for Fight"""

    report_id = db.Column(db.String(64), primary_key=True)

    start_time = db.Column(db.BigInteger, default=0)
    title = db.Column(db.Unicode(128))
    guild = ""
    realm = ""
    region = ""

    zone = sqlalchemy.orm.relationship("RaidZone")
    zone_id = db.Column(db.Integer, db.ForeignKey("raid_zone.id"))

    # children
    fights = sqlalchemy.orm.relationship(
        "Fight",
        back_populates="report",
        cascade="all,save-update,delete,delete-orphan",
        lazy="joined"
    )
    # players = sqlalchemy.orm.relationship("Player", back_populates="report")
    players = association_proxy("fights", "players")
    casts = association_proxy("fights", "casts")

    @property
    def unique_players(self):
        all_players = utils.flatten(self.players)
        all_players = {p.source_id: p for p in all_players}
        return all_players.values()

    @property
    def used_spells(self):

        all_spells = {spell.spell_id : spell for player in self.unique_players for spell in player.used_spells}
        return all_spells.values()


    @property
    def report_url(self):
        return f"https://www.warcraftlogs.com/reports/{self.report_id}"


class Fight(db.Model):
    """Basically a pull."""

    id = db.Column(db.Integer, primary_key=True)

    # parent report
    report_id = db.Column(db.String(64), db.ForeignKey("report.report_id", ondelete="cascade"))
    report = sqlalchemy.orm.relationship("Report", back_populates="fights")

    fight_id = db.Column(db.Integer)
    start_time = db.Column(db.BigInteger)
    end_time = db.Column(db.BigInteger)
    percent = db.Column(db.Float, default=0)

    boss_id = db.Column(db.Integer, db.ForeignKey("raid_boss.boss_id"))
    boss = sqlalchemy.orm.relationship("RaidBoss", back_populates="fights")

    # children
    players = sqlalchemy.orm.relationship("Player", back_populates="fight", lazy="joined")
    casts = association_proxy("players", "casts")

    def __repr__(self):
        return f"Fight({self.report.report_id}, id={self.fight_id}, players={len(self.players)})"

    ##########################
    # Attributes

    @property
    def duration(self):
        return self.end_time - self.start_time

    @property
    def duration_fmt(self):
        return utils.format_time(self.duration)

    @property
    def report_url(self):
        return f"{self.report.report_url}#fight={self.fight_id}"

    @property
    def percent_color(self):

        if self.percent < 3:
            return "astounding"
        if self.percent < 10:
            return "legendary"
        if self.percent < 25:
            return "epic"
        if self.percent < 50:
            return "rare"
        if self.percent < 75:
            return "uncommon"
        return "common"

    ##########################
    # Query

    async def load_players(self, source_ids=[]):
        logger.info(f"source_ids: {source_ids}")

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
        logger.info("Hey")
        print("Hey 2")
        if not players_data:
            return

        total_damage = players_data.get("damageDone", [])
        total_healing = players_data.get("healingDone", [])

        # player_by_id = {}  # TODO: add to FightClass
        for composition_data in players_data.get("composition", []):
            source_id = composition_data.get("id")


            class_name = composition_data.get("type")
            wow_class = WowClass.query.filter_by(name=class_name).first()
            if not wow_class:
                logger.warning("Unknown Class: %s", class_name)
                continue

            spec_data = composition_data.get("specs", [])
            if not spec_data:
                logger.warning("Player has no spec: %s", composition_data.get("name"))
                continue

            spec_data = spec_data[0]
            spec_name = spec_data.get("spec")


            spec = WowSpec.query.join(WowSpec.wow_class) # join the class so we can filter
            spec = spec.filter(WowClass.name == class_name)
            spec = spec.filter(WowSpec.name == spec_name)
            spec = spec.first()

            # Person.query.join(Person.address).filter(Adress.city == 'Paris').all()
            # player.wow_spec = spec

            # self.players.append(player)
            if not spec:
                logger.warning("Unknown Spec: %s", spec_name)
                continue

            # Get Total Damage or Healing
            spec_role = spec_data.get("role")
            total_data = total_healing if spec_role == "healer" else total_damage
            total = 0
            for data in total_data:
                if data.get("id", -1) == source_id:
                    total = data.get("total", 0) / (self.duration / 1000)
                    break

            player = Player()
            player.name = composition_data.get("name")
            player.total = total
            player.fight = self
            player.source_id = source_id
            player.spec = spec
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
            print("cast_data", cast_data)

            source_id = cast_data["sourceID"]
            player = player_by_id.get(source_id)
            if not player:
                continue

            cast = Cast()
            cast.player = player
            # cast.fight = self
            cast.timestamp = cast_data["timestamp"]
            cast.spell_id = cast_data["abilityGameID"]

        return
        # remove players with no casts
        # self.players = [p for p in self.players if p.casts]

    async def fetch(self, client, spells=(), extra_filter=""):
        # we need to fetch the fight itself
        if self.start_time <= 0:
            await self.fetch_fight_data()

        query = self._build_query(spells=spells, extra_filter=extra_filter)
        data = await client.query(query)
        self._process_query_data(data)


class Player(db.Model):
    """a player in a given fight.

    TODO:
        rename to actor?

    """
    id = db.Column(db.Integer, primary_key=True)

    report = association_proxy("fight", "report")

    # parent fight
    fight = sqlalchemy.orm.relationship("Fight", back_populates="players")
    fight_id = db.Column(db.Integer, db.ForeignKey("fight.id", ondelete="cascade"))

    # the actual player
    source_id = db.Column(db.Integer)  # TODO: rename?
    name = db.Column(db.Unicode(12)) # names can be max 12 chars
    total = db.Column(db.Integer)

    spec = sqlalchemy.orm.relationship("WowSpec", lazy="joined")
    spec_id = db.Column(db.Integer, db.ForeignKey("wow_spec.id"))

    # children
    casts = sqlalchemy.orm.relationship("Cast", back_populates="player", cascade="all,save-update,delete,delete-orphan")

    def __repr__(self):
        return f"Player({self.name} spec={self.spec.name} id={self.source_id} casts={len(self.casts)})"

    @property
    def report_url(self):
        return f"{self.fight.report_url}&source={self.source_id}"

    @property
    def used_spells(self):
        spells = {cast.spell.spell_id: cast.spell for cast in self.casts}
        return spells.values()

    def get_casts_query(self):
        """Build a query to fetch the casts done by this player."""
        print("STILL USED??? player.get_casts_query")
        spell_ids = ",".join(str(s.spell_id) for s in self.spec.spells)
        filter_expression = f"source.name='{self.name}' and ability.id in ({spell_ids})"

        return utils.shrink_text(f"""\
        reportData
        {{
            report(code: "{self.report.report_id}")
            {{
                casts: events(
                    fightIDs: {self.fight.fight_id},
                    startTime: {self.fight.start_time},
                    endTime: {self.fight.end_time},
                    dataType: Casts,
                    filterExpression: "{filter_expression}"
                ) {{data}}
            }}
        }}
        """)


class Cast(db.Model):
    """docstring for Cast"""

    id = db.Column(db.Integer, primary_key=True)

    # parent player
    player_id = db.Column(db.Integer, db.ForeignKey("player.id", ondelete="cascade"))
    player = sqlalchemy.orm.relationship("Player", back_populates="casts")

    timestamp = db.Column(db.Integer)

    spell = sqlalchemy.orm.relationship("WowSpell", lazy="joined")
    spell_id = db.Column(db.Integer, db.ForeignKey("wow_spell.spell_id"))

    fight = association_proxy("player", "fight")
    report = association_proxy("fight", "report")

    def __repr__(self):
        return f"Cast({self.spell_id}, at={self.time_fmt})"

    @property
    def time(self):
        return self.timestamp - self.fight.start_time

    @property
    def time_fmt(self):
        return utils.format_time(self.time)
