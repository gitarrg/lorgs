

from lorgs import data
from lorgs.models import encounters


def test_1():

    # zone = encounters.RaidZone(26, "Castle Nathria")
    # print(zone)
    # print(data.DEFAULT_BOSS)

    for boss in data.BOSSES:
        print(boss)




if __name__ == '__main__':
    test_1()
