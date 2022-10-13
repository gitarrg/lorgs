#!/usr/bin/env python
"""Main Entrypoint to create the Backend-APP."""

# IMPORT THIRD PARTY LIBRARIES
import fastapi

# IMPORT LOCAL LIBRARIES
from lorgs import data   # pylint: disable=unused-import
from lorgs import db  # pylint: disable=unused-import
from lorgs.routes import api


def create_app():
    """Create and return a new QuartApp-Instance.

    Returns:
        <Quart>: the new Quart-app instance

    """

    # Quart
    app = fastapi.FastAPI(
        docs_url="/api/docs",
        openapi_url="/api/openapi.json",  # must be in "/api" so the AppEngine route works
    )
    app.include_router(api.router, prefix="/api")
    return app
