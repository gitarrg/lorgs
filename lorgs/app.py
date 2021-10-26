#!/usr/bin/env python
"""Main Entrypoint to create the FlaskAPP."""

# IMPORT STANDARD LIBRARIES
import os

# IMPORT THIRD PARTY LIBRARIES
import flask

# IMPORT LOCAL LIBRARIES
from lorgs import db  # pylint: disable=unused-import
from lorgs import data   # pylint: disable=unused-import
from lorgs import cache
from lorgs.routes import api


def create_app():
    """Create and return a new QuartApp-Instance.

    Returns:
        <Quart>: the new Quart-app instance

    """
    # Quart
    app = flask.Flask(__name__)

    config_name = os.getenv("LORGS_CONFIG_NAME") or "lorgs.config.DevelopmentConfig"
    app.config.from_object(config_name)

    if app.config["LORRGS_DEBUG"]:
        from flask_cors import CORS
        cors = CORS(app)

    # Blueprints
    app.register_blueprint(api.blueprint, url_prefix="/api")

    cache.init_app(app)
    return app
