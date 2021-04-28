#!/usr/bin/env python
"""Main Entrypoint to create the FlaskAPP."""

# IMPORT STANDARD LIBRARIES
import os

# IMPORT THIRD PARTY
import flask

# IMPORT LOCAL LIBS
from lorgs import db
from lorgs import routes
from lorgs import utils


class Config:

    # Flask Main
    SECRET_KEY = os.environ.get("SECRET_KEY") or "giga-secret_key-nobody-will-ever-find-out"

    # SQLAlchemy
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI") or 'sqlite://'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        # "echo": True,
    }
    # SEND_FILE_MAX_AGE_DEFAULT = 0  # for DEV. updates static files

    GOOGLE_ANALYTICS_ID = "G-Y92VPCY6QW"


def create_app(config_obj=None):
    """Create and return a new FlaskApp-Instance.

    Args:
        config_obj(obj, optional): Object used to load config values.
            default will call `config.get_config()`

    Returns:
        <Flask>: the new flask-app instance

    """
    # create APP
    app = flask.Flask(__name__)
    app.config.from_object(config_obj or Config)

    # configure jina
    app.jinja_env.trim_blocks = True
    app.jinja_env.lstrip_blocks = True
    app.jinja_env.filters["format_time"] = utils.format_time
    app.jinja_env.filters["format_big_number"] = utils.format_big_number


    db.init_app(app)

    app.register_blueprint(routes.BP, url_prefix="/")

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0")
