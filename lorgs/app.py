#!/usr/bin/env python
"""Main Entrypoint to create the Backend-APP."""

# IMPORT STANDARD LIBRARIES
import os

# IMPORT THIRD PARTY LIBRARIES
import fastapi

# IMPORT LOCAL LIBRARIES
from lorgs import cache
from lorgs import config
from lorgs import data   # pylint: disable=unused-import
from lorgs import db  # pylint: disable=unused-import
from lorgs.routes import api



def get_config(name=""):
    name = name or os.getenv("LORGS_CONFIG_NAME") or "lorgs.config.DevelopmentConfig"
    if name == "lorgs.config.ProductionConfig":
        return config.ProductionConfig

    return config.DevelopmentConfig


def allow_cors(app):
    from fastapi.middleware.cors import CORSMiddleware
    app.add_middleware(CORSMiddleware, allow_origins="*")


def create_app():
    """Create and return a new QuartApp-Instance.

    Returns:
        <Quart>: the new Quart-app instance

    """
    config_obj = get_config()

    # Quart
    app = fastapi.FastAPI()
    cache.init(config_obj)
    app.include_router(api.router, prefix="/api")


    if config_obj.LORRGS_DEBUG:
        allow_cors(app)

    return app
