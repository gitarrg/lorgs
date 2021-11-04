import unittest
from unittest import mock


from lorgs import utils
from lorgs.models.raid_boss import RaidBoss
from lorgs.models.raid_zone import RaidZone




class TestRaidBoss():


    def test__preprocess_query_results__end_event(self):

        zone = RaidZone(id=1, name="TestZone")
        boss = RaidBoss(zone=zone, id=10, name="TestBoss")
        boss.add_event(spell_id=100, until={"spell_id": 200})

        query_result = {
            'report': {
                'events': {
                    'data': [
                        {'timestamp': 500, 'type': 'cast', 'abilityGameID': 100},
                        {'timestamp': 800, 'type': 'cast', 'abilityGameID': 200},
                    ]
                }
            }
        }

        processed = boss.preprocess_query_results(query_result)

        casts = utils.get_nested_value(processed, "report", "events", "data") or []
        assert len(casts) == 1

        cast = casts[0]
        assert cast.get("duration") == 300

    def test__preprocess_query_results__multiple_casts_with_end_event(self):

        zone = RaidZone(id=1, name="TestZone")
        boss = RaidBoss(zone=zone, id=10, name="TestBoss")
        boss.add_event(spell_id=100, until={"spell_id": 200})

        query_result = {
            'report': {
                'events': {
                    'data': [
                        {'timestamp': 100, 'type': 'cast', 'abilityGameID': 100},
                        {'timestamp': 110, 'type': 'cast', 'abilityGameID': 200},
                        {'timestamp': 200, 'type': 'cast', 'abilityGameID': 100},
                        {'timestamp': 230, 'type': 'cast', 'abilityGameID': 200},
                    ]
                }
            }
        }

        processed = boss.preprocess_query_results(query_result)

        casts = utils.get_nested_value(processed, "report", "events", "data") or []
        assert len(casts) == 2
        assert casts[0].get("duration") == 10
        assert casts[1].get("duration") == 30
