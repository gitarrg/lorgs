"""Datastore using S3."""

# IMPORT STANDARD LIBRARIES
import json
import os
import typing

# IMPORT THIRD PARTY LIBRARIES
from botocore.exceptions import ClientError
import boto3
import datetime
import pydantic

# IMPORT LOCAL LIBRARIES
from lorgs.lib.s3_store import errors


T = typing.TypeVar("T", bound="BaseModel")


s3_client = boto3.client('s3')


def serialize_value(value: typing.Any) -> typing.Any:
    if isinstance(value, datetime.datetime):
        return value.isoformat()
    return value


def serialize_dataclass(data: list[tuple[str, typing.Any]]) -> dict[str, typing.Any]:
    d = {}
    for name, value in data:
        d[name] = serialize_value(value)
    return d


def to_snake_case(name) -> str:
    return "".join("_%s" % c if c.isupper() else c for c in name).strip("_").lower()


class BaseModel(pydantic.BaseModel):

    bucket: typing.ClassVar[str] = os.getenv("DATA_BUCKET") or "lorrgs"
    key_fmt: typing.ClassVar[str]

    store: typing.ClassVar = boto3.client('s3')

    @classmethod
    def get_key(cls, **kwargs: typing.Any) -> str:
        """Generate a `key` based on the given `kwargs`."""
        key = cls.key_fmt.format(**kwargs).lower()
        table = to_snake_case(cls.__name__)
        return f"{table}/{key}"

    @property
    def key(self) -> str:
        """Object Key for this Instance."""
        return self.get_key(**self.dict())

    ############################################################################
    # S3: in/out
    #

    @typing.overload
    @classmethod
    def get(cls: typing.Type[T], create: typing.Literal[True], **kwargs: typing.Any) -> T:
        ...

    @typing.overload
    @classmethod
    def get(cls: typing.Type[T], create: bool = False, **kwargs: typing.Any) -> typing.Optional[T]:
        ...

    @classmethod
    def get(cls: typing.Type[T], create: bool = False, **kwargs: typing.Any) -> typing.Optional[T]:
        """Get an Item from the Store."""
        key = cls.get_key(**kwargs)

        try:
            data = s3_client.get_object(Bucket=cls.bucket, Key=key)
        except ClientError:
            data = None

        # data found --> parse and return
        if data:
            body = data["Body"]
            return cls.parse_raw(body.read())

        # not data --> create new instance
        if create:
            return cls(**kwargs)

        # no data + no create --> :(
        raise errors.NotFound(f"Invalid Key: {key}")

    def save(self) -> None:
        data = json.dumps(self.dict())

        # self.s3_object.put(
        s3_client.put_object(
            Bucket=self.bucket,
            Key=self.key,
            Body=data,
            ContentType="application/json",
            ACL="public-read",
        )
