"""Custom Stubs for mongoengine."""
# pylint: disable=unused-argument
# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=multiple-statements

from typing import Any, Generic, Type, TypeVar, Optional


T = TypeVar('T', bound="Document")


class QuerySet(Generic[T]):

    def first(self) -> Optional[T]:
        ...

    def exclude(self, *args: Any) -> list[T]:
        ...


class Document:

    @classmethod
    def objects(cls: Type[T], **kwargs: Any) -> QuerySet[T]: ...

    def __init__(self, **kwargs: Any) -> None: ...

    def save(self: T, **kwargs: Any) -> T: ...


##################################
# Fields

class StringField(str):

    def __new__(cls, **kwargs: Any): ...

    def __init__(self, **kwargs: Any) -> None: ...


def __getattr__(name: str) -> Any: ...
