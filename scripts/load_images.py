#!/usr/bin/env python
from __future__ import annotations

# IMPORT STANDARD LIBRARIES
import os

# IMPORT THIRD PARTY LIBRARIES
import boto3
import requests

# IMPORT LOCAL LIBRARIES
from lorgs import data
from lorgs.models.wow_potion import WowPotion
from lorgs.models.wow_spell import WowSpell
from lorgs.models.wow_trinket import WowTrinket


# S3_CLIENT = boto3.client("s3")
S3 = boto3.resource("s3")


BUCKET_NAME = os.getenv("BUCKET_NAME", "assets2.lorrgs.io")
BUCKET = S3.Bucket(BUCKET_NAME)


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


# list of all the "types" of Spells
# TODO: find a way to create this dynamically?
spell_types: set[type[WowSpell]] = {
    WowSpell,
    WowTrinket,
    WowPotion,
}


spells = []
for spell_type in spell_types:
    spells += spell_type.list()


for spell in spells:
    icon = spell.icon

    if not icon:
        print(f"spell: {spell} has no icon.")
        continue

    if icon in images:
        continue

    print(f"uploading: {icon} for {spell.name}")
    upload(icon)
