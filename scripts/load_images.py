#!/usr/bin/env python
# IMPORT THIRD PARTY LIBRARIES
import boto3
import requests

# IMPORT LOCAL LIBRARIES
from lorgs import data
from lorgs.models.wow_spell import WowSpell


# S3_CLIENT = boto3.client("s3")
S3 = boto3.resource("s3")


BUCKET = S3.Bucket("lorrgs-assets")

FOLDER = "images/spells/"


def get_images(folder: str) -> list[str]:
    images = [obj.key for obj in BUCKET.objects.filter(Prefix=folder)]
    images = [img for img in images if not img.endswith(".webp")]
    images = [img[len(folder) :] for img in images]
    return images


def upload(filname: str) -> None:
    # Download the file from the HTTP URL
    url = f"https://wow.zamimg.com/images/wow/icons/large/{filname}"
    response = requests.get(url)
    if not response:
        response.raise_for_status()

    # Upload to S3
    BUCKET.put_object(
        Body=response.content,
        Key=f"{FOLDER}{filname}",
        ContentType="image/jpeg",
        CacheControl="public, max-age=31536000, immutable",
    )


################################################################################

images = get_images(FOLDER)

spells = WowSpell.list() + WowTrinket.list()

for spell in spells:
    icon = spell.icon

    if not icon:
        print(f"spell: {spell.name} has no icon.")
        continue

    if icon in images:
        continue

    print(f"uploading: {icon} for {spell.name}")
    upload(icon)
