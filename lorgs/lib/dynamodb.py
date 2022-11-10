"""Client to store Objects in DynamoDB."""

# IMPORT STANDARD LIBRARIES
import decimal
import json
import typing

# IMPORT THIRD PARTY LIBRARIES
import boto3
import pydantic
from boto3.dynamodb.conditions import Attr

# IMPORT LOCAL LIBRARIES
from lorgs import utils
from lorgs.logger import Timer

if typing.TYPE_CHECKING:
    from mypy_boto3_dynamodb.service_resource import Table


dynamodb = boto3.resource("dynamodb")


TBaseModel = typing.TypeVar("TBaseModel", bound="BaseModel")


class BaseModel(pydantic.BaseModel):

    pkey_name: typing.ClassVar[str] = "pk"
    skey_name: typing.ClassVar[str] = "sk"
    pkey: typing.ClassVar[str] = "{id}"
    skey: typing.ClassVar[str] = ""

    def __init__(self, **kwargs: typing.Any) -> None:
        super().__init__(**kwargs)
        self.post_init()

    def post_init(self) -> None:
        """Hook to implement some custom initialization logic."""

    @classmethod
    def get_table_name(cls) -> str:
        return utils.to_snake_case(cls.__name__)

    @classmethod
    def get_table(cls) -> "Table":
        return dynamodb.Table(cls.get_table_name())

    @classmethod
    def get_keys(cls, **kwargs) -> dict[str, str]:
        keys = {cls.pkey_name: cls.pkey.format(**kwargs)}
        if cls.skey_name and cls.skey:
            keys[cls.skey_name] = cls.skey.format(**kwargs)
        return keys

    ############################################################################
    # Get from DB
    #

    @classmethod
    def get(cls: typing.Type[TBaseModel], **kwargs: typing.Any) -> typing.Optional[TBaseModel]:

        table = cls.get_table()
        keys = cls.get_keys(**kwargs)

        with Timer(f"GET: {kwargs}"):
            response = table.get_item(Key=keys)
        try:
            item = response["Item"]
        except KeyError:
            return None

        obj = cls.parse_obj(item)
        return obj

    @classmethod
    def get_or_create(cls: typing.Type[TBaseModel], **kwargs: typing.Any) -> TBaseModel:
        return cls.get(**kwargs) or cls(**kwargs)

    @classmethod
    def first(cls: typing.Type[TBaseModel], **kwargs: typing.Any) -> typing.Optional[TBaseModel]:
        """Returns the first Item matching the given keywords."""

        table = cls.get_table()

        if not kwargs:
            raise ValueError("Need to provide some seach arguments.")

        expr = None
        for name, value in kwargs.items():
            attr = Attr(name).eq(value)
            if not expr:
                expr = attr
            else:
                expr = expr & attr

        response = table.scan(FilterExpression=expr)  # type: ignore
        items = response["Items"]
        if not items:
            return None

        item = items[0]
        return cls.parse_obj(item)

    ############################################################################
    # Save to DB
    #

    def save(self, exclude_unset: bool = True) -> None:

        # convert into json compatible dict
        # this back and fort serialization makes sure all complex objects
        # are converted into json compatible formats.
        # There is some work done to simplify this: https://github.com/pydantic/pydantic/discussions/4456
        data = json.loads(
            self.json(exclude_unset=exclude_unset),
            parse_float=decimal.Decimal,  # dynamodb wants floats as decimals
        )

        # insert keys
        data.update(self.get_keys(**data))

        table_name = self.get_table_name()
        table = dynamodb.Table(table_name)

        table.put_item(Item=data)
