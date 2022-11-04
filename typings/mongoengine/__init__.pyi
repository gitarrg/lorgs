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

def IntField(**kwargs: Any) -> int: ...

def StringField(**kwargs: Any) -> str: ...

def DictField(**kwargs: Any) -> dict[str, Any]: ...


def __getattr__(name: str) -> Any: ...
