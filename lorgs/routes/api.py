"""Endpoints related to the Backend/API."""

# IMPORT STANDARD LIBRARIES
import datetime

# IMPORT THIRD PARTY LIBRARIES
import flask

# IMPORT LOCAL LIBRARIES
from lorgs.routes import api_comp_rankings
from lorgs.routes import api_spec_rankings
from lorgs.routes import api_world_data
from lorgs.routes import api_user_reports


blueprint = flask.Blueprint("api", __name__, cli_group=None)


################################################################################
# Child Blueprints
blueprint.register_blueprint(api_comp_rankings.blueprint, url_prefix="/")
blueprint.register_blueprint(api_spec_rankings.blueprint, url_prefix="/")
blueprint.register_blueprint(api_world_data.blueprint, url_prefix="/")
blueprint.register_blueprint(api_user_reports.blueprint, url_prefix="/user_reports")


################################################################################


@blueprint.route("/<path:path>")
def page_not_found(path):
    return "Invalid Route", 404


@blueprint.get("/ping")
def ping():
    return {"reply": "Hi!", "time": datetime.datetime.utcnow().isoformat()}
