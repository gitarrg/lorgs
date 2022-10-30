"""Adds a CORS Middleware."""

import os
# import typing

import fastapi
from fastapi.middleware.cors import CORSMiddleware

# TMP FIX
DEBUG = os.getenv("DEBUG")


def init(app: fastapi.FastAPI, enabled=DEBUG):

    if not enabled:
        return

    origins = ["https://lorrgs.io"]
    if DEBUG:
        origins.append("*")

    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["POST", "GET"],
        allow_headers=["*"],
        max_age=3600,
    )


