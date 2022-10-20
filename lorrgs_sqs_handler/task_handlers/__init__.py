import typing

from . import send_discord_message
from . import load_user_report


TASK_HANDLERS : typing.Dict[str, typing.Callable] = {

    "unknown": send_discord_message.main,
    "load_user_report": load_user_report.main,
}
