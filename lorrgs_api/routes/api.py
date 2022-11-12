"""Endpoints related to the Backend/API."""

# IMPORT THIRD PARTY LIBRARIES
import fastapi

# IMPORT LOCAL LIBRARIES
# from lorrgs_api.routes import api_comp_rankings
from lorrgs_api.routes import api_spec_rankings
from lorrgs_api.routes import api_tasks
from lorrgs_api.routes import api_user_reports
from lorrgs_api.routes import api_world_data
from lorrgs_api.routes import auth
from lorrgs_api.routes import debug


router = fastapi.APIRouter()


################################################################################
# Child Blueprints
# router.include_router(api_comp_rankings.router)
router.include_router(api_spec_rankings.router)
router.include_router(api_tasks.router)
router.include_router(api_user_reports.router, prefix="/user_reports")
router.include_router(api_world_data.router)
router.include_router(debug.router)
router.include_router(auth.router, prefix="/auth")


################################################################################


@router.get("/error")
def error():
    """Route to test error handling"""
    raise ValueError("something went wrong!")


@router.get("/")
@router.get("/{path:path}")
def page_not_found(path=""):
    return "Invalid Route", 404
