"""Store Objects in S3."""

# IMPORT STANDARD LIBRARIES
import json
import os
import typing

# IMPORT THIRD PARTY LIBRARIES
import boto3
from botocore.exceptions import ClientError

# IMPORT LOCAL LIBRARIES
from lorgs.logger import Timer
from lorgs.models.base import base


class S3Model(base.BaseModel):

    bucket: typing.ClassVar[str] = os.getenv("DATA_BUCKET") or "lorrgs"
    s3client: typing.ClassVar = boto3.client("s3")

    @classmethod
    def get_key(cls, **kwargs) -> str:
        key = super().get_key(**kwargs)
        return f"{cls.get_table_name()}/{key}"

    ############################################################################
    # S3: in/out
    #

    @classmethod
    def get_json(cls, **kwargs: typing.Any) -> typing.Any:
        key = cls.get_key(**kwargs)
        try:
            with Timer(f"s3.get_raw: {key}"):
                data = cls.s3client.get_object(Bucket=cls.bucket, Key=key)
        except ClientError:
            raise KeyError("Invalid Key: %s", key)

        body = data["Body"]
        return json.loads(body.read())

    @classmethod
    def get(cls, **kwargs: typing.Any) -> typing.Optional["S3Model"]:
        """Get an Item from the Store."""
        try:
            content = cls.get_json(**kwargs)
        except KeyError:
            return None
        return cls.construct(**content)

    def save(self, exclude_unset=True, **kwargs: typing.Any) -> None:

        key = self.get_key(**self.dict())
        data = self.json(exclude_unset=exclude_unset, **kwargs)
        print("saving to S3", self.bucket, key)
        self.s3client.put_object(
            Bucket=self.bucket,
            Key=key,
            Body=data,
            ContentType="application/json",
        )
