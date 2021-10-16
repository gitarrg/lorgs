"""Endpoints related to the Backend/API."""

# IMPORT STANDARD LIBRARIES
import datetime

# IMPORT THIRD PARTY LIBRARIES
import flask

# IMPORT LOCAL LIBRARIES
from lorgs.routes import api_comp_rankings
from lorgs.routes import api_spec_rankings
from lorgs.routes import api_world_data


blueprint = flask.Blueprint("api", __name__, cli_group=None)


@blueprint.after_request
def add_headers(response):
    # allow cors for local dev, so I can run the webpack live server on a different port.
    if flask.current_app.config["LORRGS_DEBUG"]:
        response.headers["Access-Control-Allow-Origin"] = "*"
    return response


################################################################################
# Child Blueprints
blueprint.register_blueprint(api_comp_rankings.blueprint, url_prefix="/")
blueprint.register_blueprint(api_spec_rankings.blueprint, url_prefix="/")
blueprint.register_blueprint(api_world_data.blueprint, url_prefix="/")


################################################################################


@blueprint.route("/<path:path>")
def page_not_found(path):
    return "Invalid Route", 404


@blueprint.get("/ping")
def ping():
    return {"reply": "Hi!", "time": datetime.datetime.utcnow().isoformat()}
