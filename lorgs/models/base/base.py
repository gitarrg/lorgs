"""Base Class for all Models in our System."""
from __future__ import annotations

# IMPORT STANDARD LIBRARIES
from datetime import date, datetime, time, timedelta
from typing import Any, Callable, ClassVar, Optional, Type, TypeVar

# IMPORT THIRD PARTY LIBRARIES
import pydantic
from pydantic.datetime_parse import parse_date, parse_datetime, parse_duration, parse_time

# IMPORT LOCAL LIBRARIES
from lorgs import utils


T = TypeVar("T", bound="BaseModel")


CONVERTERS: dict[type, Callable] = {
    str: str,
    float: float,
    int: int,
    datetime: parse_datetime,
    date: parse_date,
    time: parse_time,
    timedelta: parse_duration,
}


class BaseModel(pydantic.BaseModel):
    """Base Class for all Models in our System."""

    key: ClassVar[str] = "{id}"

    def post_init(self) -> None:
        """Hook to implement some custom initialization logic."""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.post_init()

    @classmethod
    def construct(cls: Type[T], _fields_set=None, *, __recursive__=True, **values) -> T:
        # based on https://github.com/pydantic/pydantic/issues/1168
        if not __recursive__:
            return super().construct(_fields_set, **values)

        m = cls.__new__(cls)

        fields_values: dict[str, Any] = {}
        for name, field in cls.__fields__.items():
            if name in values:
                value = values[name]

                # Field is a nested Model
                if issubclass(field.type_, BaseModel):

                    if field.shape == 2:  # SHAPE_LIST
                        fields_values[name] = [field.type_.construct(**v, __recursive__=True) for v in value]
                    else:
                        fields_values[name] = field.outer_type_.construct(**value, __recursive__=True)
                else:
                    converter = CONVERTERS.get(field.type_)
                    if converter:
                        if field.shape == 2:  # SHAPE_LIST
                            fields_values[name] = [converter(v) for v in value]
                        else:
                            fields_values[name] = converter(value)
                    else:
                        fields_values[name] = value

            elif not field.required:
                fields_values[name] = field.get_default()

        object.__setattr__(m, "__dict__", fields_values)
        if _fields_set is None:
            _fields_set = set(values.keys())
        object.__setattr__(m, "__fields_set__", _fields_set)
        m._init_private_attributes()
        m.post_init()
        return m

    @classmethod
    def get_table_name(cls) -> str:
        return utils.to_snake_case(cls.__name__)

    @classmethod
    def get_key(cls, **kwargs) -> str:
        """Generate a `key` based on the given `kwargs`."""
        kwargs.setdefault("table_name", cls.get_table_name())
        return cls.key.format(**kwargs)

    @classmethod
    def get(cls: Type[T], **kwargs: Any) -> Optional[T]:
        ...

    @classmethod
    def get_or_create(cls: Type[T], **kwargs: Any) -> T:
        return cls.get(**kwargs) or cls(**kwargs)

    def save(self) -> None:
        ...
