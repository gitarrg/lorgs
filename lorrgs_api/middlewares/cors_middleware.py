"""Adds a CORS Middleware."""

import os
import typing

if typing.TYPE_CHECKING:
    import fastapi


# TMP FIX
DEBUG = True # os.getenv("DEBUG")


def init(app: "fastapi.FastAPI", enabled=DEBUG):

    if not enabled:
        return

    from fastapi.middleware.cors import CORSMiddleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["POST", "GET"],
        allow_headers=["*"],
        max_age=3600,
    )


