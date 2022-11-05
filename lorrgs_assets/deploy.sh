#!/usr/bin/env bash

aws s3 sync \
    lorrgs_assets \
    s3://lorrgs-assets \
    --cache-control 'public, max-age=31536000, immutable' \
    --exclude "*" \
    --include "*.png" \
    --include "*.jpg" \
    --include "*.jpeg" \
