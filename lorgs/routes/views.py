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
@cache.cached()
def index():
    """Render the main index page."""
    kwargs = {}
    kwargs["boss"] = data.DEFAULT_BOSS
    kwargs["roles"] = data.ROLES
    return flask.render_template("index.html", **kwargs)


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


@blueprint.route("/comp_ranking/<path:subpath>")
@blueprint.route("/spec_ranking/<path:subpath>")
@cache.cached()
def react_app(**kwargs):
    """Route for all pages that are fully managed by react."""
    return flask.render_template("app.html")
