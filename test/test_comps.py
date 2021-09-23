#!/usr/bin/env python
"""Script to create all Spells."""

import asyncio

# IMPORT THIRD PARTY LIBRARIES
# import sqlalchemy as sa
# from sqlalchemy.ext.declarative import declared_attr
import dotenv
dotenv.load_dotenv() # pylint: disable=wrong-import-position
import mongoengine as me

# IMPORT LOCAL LIBRARIES
from lorgs import db
from lorgs import data
from lorgs.models import warcraftlogs_base
from lorgs.models import warcraftlogs_comps
from lorgs.models.specs import WowClass
from lorgs.models.specs import WowRole
from lorgs.models.specs import WowSpec



# heal.4%7C2.4.1,6.1.1,7.1.1,9.3.1

"""
class TopCompFightPlayer(warcraftlogs_base.BasePlayer):
    pass

    # __tablename__ = "comp_fight_player"

    @declared_attr
    def fight_id(cls):
        return sa.Column(sa.Integer(), sa.ForeignKey("comp_fight.id"))

    @declared_attr
    def fight(cls):
        return sa.orm.relationship("TopCompFight")
"""
'''

class TopCompFight(warcraftlogs_base.BaseFight):
    """docstring for Fight"""

    # player_cls = TopCompFightPlayer
    # comp = sa.orm.relationship("Comp", back_populates="fights")
    # comp_id = sa.Column(sa.Integer, sa.ForeignKey("comp.id"))
    # @declared_attr
    # def players(cls):
    #     return sa.orm.relationship(
    #         "TopCompFightPlayer",
    #         back_populates="fight",
    #         cascade="all,delete,delete-orphan",
    #     )


class Comp(me.Document, warcraftlogs_base.wclclient_mixin):
    """docstring for Comp"""

    # __tablename__ = "comp"

    name = me.StringField(max_length=200, required=True)

    # id = sa.Column(sa.Integer, primary_key=True)
    # fights = sa.orm.relationship(
    #     "TopCompFight",
    #     back_populates="comp",
    #     cascade="all,delete,delete-orphan",
    #     lazy="joined"
    # )
    report_search = me.StringField(default="")

    fight_filter = me.ListField(me.StringField())

    fights = me.ListField(me.EmbeddedDocumentField(warcraftlogs_base.BaseFight))

    """
    fight_filter = [
        "source.role='healer'",
        "ability.id in (740, 323764, 197721)"
    ]
    """

    # def __init__(self):
    #     super().__init__()
    #     self.fights = []



    async def load(self, boss_id):
        # load top fights
        await self.find_fights(boss_id)
        await TopCompFight.load_many(self.fights, filters=self.fight_filter)


'''

def create_comps():

    """
    name = "healer-hpala-disc-rshaman-rdruid"
    comp = warcraftlogs_comps.CompConfig.get_or_create(name=name)
    comp.report_search = "heal.4 | 2.4.1, 6.1.1, 7.1.1, 9.3.1".replace(" ", "")
    comp.casts_filter = "source.role='healer'"

    comp.specs = [data.PALADIN_HOLY, data.PRIEST_DISCIPLINE, data.SHAMAN_RESTORATION, data.DRUID_RESTORATION]
    comp.save()
    """
    name = "any-heal"
    comp = warcraftlogs_comps.CompConfig.get_or_create(name=name)
    comp.report_search = ""
    comp.casts_filter = "source.role='healer'"
    comp.specs = data.HEAL.specs
    comp.save()

    name = "any_heal_with_rdruid"
    comp = warcraftlogs_comps.CompConfig.get_or_create(name=name)
    comp.report_search = "2.4.1"
    comp.casts_filter = "source.role='healer'"
    comp.specs = data.HEAL.specs
    comp.save()

    name = "any_heal_with_hpriest"
    comp = warcraftlogs_comps.CompConfig.get_or_create(name=name)
    comp.report_search = "7.2.1"
    comp.casts_filter = "source.role='healer'"
    comp.specs = data.HEAL.specs
    comp.save()

    name = "any_heal_without_disc"
    comp = warcraftlogs_comps.CompConfig.get_or_create(name=name)
    comp.report_search = "7.1.0"
    comp.casts_filter = "source.role='healer'"
    comp.specs = data.HEAL.specs
    comp.save()


    # print(comp)
    # print(comp.id)
    # print(comp.specs)

    """
    comp.fight_filter = [
        "source.role='healer'",
        "ability.id in (740, 323764, 197721)"
    ]
    """
    return


async def load():

    comp_name = "any-heal"
    comp_config = warcraftlogs_comps.CompConfig.objects(name=comp_name).first()

    # bosses = data.CASTLE_NATHRIA_BOSSES
    bosses = [data.TARRAGRUE]

    for boss in bosses:
        print("LOADING", boss)
        scr = await comp_config.load_reports(boss_slug=boss.name_slug)
        scr.save()
        comp_config.save()


        for report in scr.reports:
            print(report)
            for fight in report.fights:
                print("\t", fight)

    """
    # print(comp.boss_reports)
    comp.boss_reports[comp_ranking.boss_slug] = comp_ranking
    comp_config.save()
    """


async def main():

    create_comps()
    # await load()

    # comp_ranking = warcraftlogs_comps.CompRating.objects.first()
    # print(comp_ranking.report_url)
    # for spell in spec_ranking.spells_used:
    #     print(spell.group, spell)



if __name__ == '__main__':
    asyncio.run(main())
