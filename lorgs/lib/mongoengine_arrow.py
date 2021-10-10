"""Copy/Pasted due to dependency conflict with arrow."""

__version__ = "0.1.3"

from mongoengine import fields
import datetime
import arrow


class ArrowDateTimeField(fields.DateTimeField):
    def to_mongo(self, value):
        if isinstance(value, arrow.arrow.Arrow):
            value = value.to("utc").naive

        value = super().to_mongo(value)

        return value

    def to_python(self, value):
        value = super().to_python(value)

        if isinstance(value, datetime.datetime):
            if value.tzinfo is None:
                return arrow.get(value).replace(tzinfo="utc")
            else:
                return arrow.get(value)

        return arrow.get(value)

    def __set__(self, instance, value):
        if isinstance(value, datetime.datetime):
            if value.tzinfo is None:
                value = arrow.get(value).replace(tzinfo="utc")
            else:
                value = arrow.get(value)

        return super().__set__(instance, value)

    def __get__(self, instance, owner):
        if instance is None:
            return self

        value = super().__get__(instance, owner)

        if value is None:
            return None

        if isinstance(value, arrow.arrow.Arrow):
            return value.to("utc")

        return None
