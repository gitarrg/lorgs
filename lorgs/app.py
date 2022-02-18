#!/usr/bin/env python
"""Main Entrypoint to create the Backend-APP."""

# IMPORT STANDARD LIBRARIES
import os

# IMPORT THIRD PARTY LIBRARIES
import fastapi
import mangum
from fastapi.middleware.cors import CORSMiddleware

# IMPORT LOCAL LIBRARIES
from lorgs import cache
from lorgs import config
from lorgs import data   # pylint: disable=unused-import
from lorgs import db  # pylint: disable=unused-import
from lorgs.routes import api


CORS_ORIGINS = [
    "*",  # fixme later
    "https://*.lorrgs-frontend.pages.dev",
]


def create_app():
    """Create and return a new QuartApp-Instance.

    Returns:
        <Quart>: the new Quart-app instance

    """
    config_obj = config.get_config()

    # Quart
    app = fastapi.FastAPI(
        docs_url="/api/docs",
        openapi_url="/api/openapi.json",  # must be in "/api" so the AppEngine route works
    )
    cache.init(config_obj)
    app.include_router(api.router, prefix="/api")

    # @app.get("/")
    # @app.get("/{path:path}")
    # async def frontend_redirect(path=""):
    #     URL = "https://lorrgs.io"
    #     url = os.path.join(URL, path)
    #     return fastapi.responses.RedirectResponse(url, status_code=301) # 301: Moved Permanently

    # Apply Cors Headers
    if config_obj.LORRGS_DEBUG:
        CORS_ORIGINS.append("*")

    # app.add_middleware(
    #     CORSMiddleware,
    #     allow_origins=CORS_ORIGINS,
    #     allow_credentials=True,
    #     allow_methods=["POST", "GET"],
	# 	allow_headers=["*"],
    #     max_age=3600,
    # )
    return app


def create_handler(*args, **kwargs):

    app = create_app()
    handler = mangum.Mangum(app)
    return handler(*args, **kwargs)
