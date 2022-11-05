"""Datastore using S3."""

# IMPORT STANDARD LIBRARIES
import os
import typing
import dataclasses
import json
from dataclasses import dataclass, field

# IMPORT THIRD PARTY LIBRARIES
import boto3
import pydantic
import datetime
import attrs
from botocore.exceptions import ClientError
# from mypy_boto3_s3.service_resource import Object

# IMPORT LOCAL LIBRARIES
from lorgs.lib.s3_store import errors
from lorgs.logger import timeit


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



class BaseModel:

    bucket: typing.ClassVar[str] = os.getenv("DATA_BUCKET") or "lorrgs" # 
    ttl: datetime.timedelta = datetime.timedelta(0)
    key_fmt: typing.ClassVar[str]

    store = boto3.client('s3')

    def __init__(self, **kwargs: typing.Any) -> None:
        ...
        # super().__init__(**kwargs)

    def dict(self) -> dict[str, typing.Any]:
        if dataclasses.is_dataclass(self):
            return dataclasses.asdict(self, dict_factory=serialize_dataclass)
        raise NotImplementedError

    @classmethod
    def get_key(cls, **kwargs: typing.Any) -> str:
        """Generate a `key` based on the given `kwargs`."""
        key = cls.key_fmt.format(**kwargs).lower()
        table = cls.__name__.lower()
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
            # content = body.read().decode("utf8")
            info = json.load(body)
            return cls(**info)
            # content = pickle.loads(bb)
            # return cls.parse_raw()

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
            Expires="", # TODO
        )
