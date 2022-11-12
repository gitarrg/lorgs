"""Object store in Memory.

This model keeps a reference to all its instance in memory using a weakref-set,
proving us with database-like access to the objects.

"""
# IMPORT STANDARD LIBRARIES
import typing
import weakref
from collections import defaultdict

# IMPORT LOCAL LIBRARIES
from lorgs import utils
from lorgs.models.base import base

T = typing.TypeVar("T", bound="MemoryModel")


class MemoryModel(base.BaseModel):
    """Model which keeps track of all created instances in memory."""

    __slots__ = ["__weakref__"]

    __instances__: typing.ClassVar[defaultdict] = defaultdict(weakref.WeakSet)

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.__instances__[type(self)].add(self)

    @classmethod
    def get(cls: typing.Type[T], **kwargs) -> typing.Optional[T]:
        instances = cls.__instances__[cls]
        return utils.get(instances, **kwargs)

    @classmethod
    def list(cls: typing.Type[T]) -> list[T]:
        return list(cls.__instances__[cls])

    def __hash__(self) -> int:
        # Restore the default implementation because pydantic overwrites it.
        return object.__hash__(self)
