"""Views/Routes for the UI/Frontend."""

# IMPORT THIRD PARTY LIBS
import flask

# IMPORT LOCAL LIBS
from lorgs import data
from lorgs.cache import cache


blueprint = flask.Blueprint(
    "ui",
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="/"
)


################################################################################
#
#   GLOBAL
#
################################################################################

@blueprint.app_errorhandler(404)
async def page_not_found(error):
    # note that we set the 404 status explicitly
    return flask.render_template("errors/404.html", error=error), 404


@blueprint.get("/")
def index():
    """Render the main index page."""
    # return flask.send_from_directory("static/_generated", "index.html")
    return "hello from flask"
    # kwargs = {}
    # kwargs["boss"] = data.TARRAGRUE
    # kwargs["roles"] = data.ALL_ROLES
    # return flask.render_template("index.html", **kwargs)


@blueprint.get("/help")
@cache.cached()
def help():
    """Render the help page."""
    return flask.render_template("help.html")


################################################################################
#
#   React Route
#
################################################################################


# @blueprint.route("/lorgmin/<path:subpath>")
# @blueprint.route("/comp_ranking/<path:subpath>")
# @blueprint.route("/spec_ranking/<path:subpath>")
# @blueprint.route("/app")
# # @cache.cached()
# def react_app(**kwargs):
#     """Route for all pages that are fully managed by react."""
#     return flask.send_from_directory("static/_generated", "index.html")
#     # return flask.render_template("index.html")

