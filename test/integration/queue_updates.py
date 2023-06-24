import dotenv

dotenv.load_dotenv()

# IMPORT LOCAL LIBRARIES
from lorgs.clients import sqs
from lorgs.data.classes import *


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
    SPECS = [
        WARRIOR_ARMS,
        WARRIOR_FURY,
        WARRIOR_PROTECTION,
    ]

    for spec in SPECS:
        load(
            spec.full_name_slug,
            boss_slug="all",
            limit=49,
            clear=True,
        )


if __name__ == "__main__":
    main()
