
# Lorrgs Assets:

This module holds any static Assets, (eg.: Images) used on [lorrgs.io](https://lorrgs.io).  
The files will be uploaded to S3 and cached via CloudFront.

We mostly store any assets strongly related to the `lorrgs.data` here. eg.; Spell- or Boss-Icons,
where the data does have a direct relation to the assets.

This allows adding new spells without updating the frontend repository.


## Conversion:

There is a lambda function monitoring the S3 Bucket and automatically converting
all uploaded `.jpg`, `.jpeg` and `.png` files to `.webp`.
