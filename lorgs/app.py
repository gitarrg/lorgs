#!/usr/bin/env python
"""Main Entrypoint to create the FlaskAPP."""

# IMPORT STANDARD LIBRARIES
import os

# IMPORT THIRD PARTY LIBRARIES
import flask

# IMPORT LOCAL LIBRARIES
from lorgs import db  # pylint: disable=unused-import
from lorgs import data   # pylint: disable=unused-import
from lorgs import utils
from lorgs import cache
from lorgs.routes import api
# from lorgs.routes import views


def create_app():
    """Create and return a new FlaskApp-Instance.

    Returns:
        <Flask>: the new flask-app instance

    """
    # Flask
    app = flask.Flask(__name__)

    config_name = os.getenv("LORGS_CONFIG_NAME") or "lorgs.config.DevelopmentConfig"
    app.config.from_object(config_name)

    # Jina
    # app.jinja_env.trim_blocks = True
    # app.jinja_env.lstrip_blocks = True
    # app.jinja_env.filters["format_time"] = utils.format_time
    # app.jinja_env.filters["format_big_number"] = utils.format_big_number
    # app.jinja_env.filters["format_timestamp"] = utils.format_timestamp

    # Blueprints
    # app.register_blueprint(views.blueprint, url_prefix="/")
    app.register_blueprint(api.blueprint, url_prefix="/api")

    cache.init_app(app)
    return app
