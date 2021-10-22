"""Classes/Functions to manage Reports injected through user interaction."""

# IMPORT STANDARD LIBRARIES
import typing

# IMPORT THIRD PARTY LIBRARIES
import arrow
import mongoengine as me

# IMPORT LOCAL LIBRARIES
from lorgs.logger import logger
from lorgs.lib import mongoengine_arrow
from lorgs.models import warcraftlogs_report


class UserReport(me.Document):
    """Shallow Wrapper around a `warcraftlogs_report.Report`.

    Most things should be managed via the Report Instance on: `self.report`

    """
    # datetime: timetamp of last update
    updated: arrow.Arrow = mongoengine_arrow.ArrowDateTimeField(default=arrow.utcnow)

    # the wrapped report object
    report: warcraftlogs_report.Report = me.EmbeddedDocumentField(warcraftlogs_report.Report)

    @classmethod
    def from_report_id(cls, report_id: str, create=False) -> typing.Union["UserReport", None]:
        """Need to split it, as otherwise the creation with nested parm does;t work"""
        user_report = cls.objects(report__report_id=report_id).first()  # pylint: disable=no-member
        if user_report:
            return user_report

        if not create:
            return None

        user_report = cls()
        user_report.report = warcraftlogs_report.Report(report_id=report_id)
        return user_report


    ################################
    # Properties
    #
    def as_dict(self):
        return {
            "updated": int(self.updated.timestamp()),
            "report": self.report.as_dict(), # pylint: disable=no-member
        }

    ################################
    # Methods
    #
    async def load(self, *args, **kwargs):
        await self.report.load(*args, **kwargs)  # pylint: disable=no-member

    async def load_fights(self, fight_ids: typing.List[int], player_ids: typing.List[int]):

        if not (fight_ids and player_ids):
            raise ValueError(f"fight or player ids missing: {fight_ids} {player_ids}")

        # for fights, we can simply filter out the fights we want.
        fights_to_load = [fight for fight in self.report.fights if fight.fight_id in fight_ids]  # pylint: disable=no-member

        ###############################
        # players are trickier..
        #
        source_players = {player.source_id: player for player in self.report.players}  # pylint: disable=no-member

        for fight in fights_to_load:
            for player_id in player_ids:
                # check if the fight already has that player loaded
                old_player = fight.get_player(source_id=player_id)
                if old_player:
                    logger.debug("found old player: %s", old_player)
                    continue

                # get the source player to copy (from the report)
                source_player = source_players.get(player_id)
                if not source_player:
                    logger.warning("no source player for id: %s", player_id)
                    continue

                # create a new player instance on the fight
                fight.add_player(
                    name=source_player.name,
                    source_id=source_player.source_id,
                    spec_slug=source_player.spec_slug,
                )

        fights_to_load = [f for f in fights_to_load if f.players]
        if fights_to_load:
            await self.report.load_many(fights_to_load)