#!/usr/bin/env python

import dotenv

dotenv.load_dotenv()

# IMPORT LOCAL LIBRARIES
from lorgs.clients import sqs
from lorgs.data.classes import *
from lorgs.data.raids import *


def load(
    spec_slug: str = "all",
    boss_slug: str = "all",
    difficulty="all",
    metric="all",
    limit=50,
    clear: bool = False,
):
    payload = {
        "task": "load_spec_rankings",
        "spec_slug": spec_slug,
        "boss_slug": boss_slug,
        "difficulty": difficulty,
        "metric": metric,
        "limit": limit,
        "clear": clear,
    }

    # print(payload)
    # from lorrgs_sqs import helpers
    # for pl in helpers.expand_keywords(payload):
    #     print(pl)
    return sqs.send_message(payload=payload)


def main() -> None:
    bosses = [
        # GNARLROOT,
        # # IGIRA,
        # VOLCOROSS,
        # COUNCIL_OF_DREAMS,
        # # LARODAR,
        # NYMUE,
        # SMOLDERON,
        # TINDRAL,
        # FYRAKK,
    ]
    bosses = AMIRDRASSIL.bosses

    specs = [
        # *ALL_SPECS,
        # *TANK.specs
        # *HEAL.specs
        # ROGUE_SUBTLETY,
        # *INT_SPECS,
        # MAGE_FROST,
        # DEATHKNIGHT_BLOOD,
        # DEMONHUNTER_HAVOC,
        # SHAMAN_ELEMENTAL,
        # SHAMAN_ENHANCEMENT,
        # SHAMAN_RESTORATION,
        PRIEST_DISCIPLINE,
        PRIEST_HOLY,
        PRIEST_SHADOW,
    ]

    for spec in specs:
        print(spec.full_name_slug)
        for boss in bosses:
            print("\t", boss.full_name_slug)
            load(
                spec.full_name_slug,
                boss_slug=boss.full_name_slug,
                limit=50,
                clear=True,
            )


if __name__ == "__main__":
    main()
