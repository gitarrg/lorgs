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
    def get(cls, **kwargs: typing.Any) -> typing.Optional["S3Model"]:
        """Get an Item from the Store."""
        key = cls.get_key(**kwargs)

        with Timer("S3.get_object"):
            try:
                data = cls.s3client.get_object(Bucket=cls.bucket, Key=key)
            except ClientError:
                return None

        # data found --> parse and return
        body = data["Body"]
        content = json.loads(body.read())
        return cls.construct(**content)

    def save(self, exclude_unset=True, **kwargs: typing.Any) -> None:

        key = self.get_key(**self.dict())
        data = self.json(exclude_unset=exclude_unset, **kwargs)

        self.s3client.put_object(
            Bucket=self.bucket,
            Key=key,
            Body=data,
            ContentType="application/json",
            ACL="public-read",
        )
