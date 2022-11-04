"""Very basic Event/Subscriber Pattern

>>> async def handler(event: Event):
>>>     print("[Handler]", event.payload["message"])
>>> 
>>> async def main() -> None:
>>>     register("my_event", handler)
>>>     await submit("my_event", message="Hello World")
>>>
>>> asyncio.run(main())
[Handler] Hello World
"""
from typing import Any, Callable, Awaitable
from dataclasses import dataclass, field
from collections import defaultdict


@dataclass
class Event:
    """An Event dispatched to the handlers."""

    name: str
    """Name/Type of the Event."""

    payload: dict[str, Any] = field(default_factory=dict)
    """Event Payload"""


handler_type = Callable[[Event], Awaitable]


handlers: defaultdict[str, set[handler_type]] = defaultdict(set)


def register(event_name: str, func: handler_type) -> None:
    """Add a new Handler for a given Event

    Args:
        event_name (str): name of the event
        func (Callable(Event)): The Handler Function
    """
    handlers[event_name].add(func)


def unregister(event_name: str, func: handler_type) -> None:
    """Removes a Handler from the given Event

    Args:
        event_name (str): name of the event
        func (Callable(Event)): The Handler Function
    """
    handlers[event_name].remove(func)


async def submit(event_name: str, **kwargs: Any) -> None:
    """Submit/Dispatch an event

    Args:
        event_name (str): name of the event
        payload (typing.Any): event payload
    """
    event = Event(name=event_name, payload=kwargs)

    for handler in handlers[event_name]:
        await handler(event)
