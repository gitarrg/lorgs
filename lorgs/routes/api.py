"""Endpoints related to the Backend/API."""

# IMPORT STANDARD LIBRARIES
import datetime

# IMPORT THIRD PARTY LIBRARIES
import fastapi

# IMPORT LOCAL LIBRARIES
from lorgs.routes import api_comp_rankings
from lorgs.routes import api_spec_rankings
# from lorgs.routes import api_tasks
from lorgs.routes import api_user_reports
from lorgs.routes import api_world_data
# from lorgs.routes import auth


router = fastapi.APIRouter()


################################################################################
# Child Blueprints
router.include_router(api_comp_rankings.router)
router.include_router(api_spec_rankings.router)
# router.include_router(api_tasks.router, prefix="/tasks")
router.include_router(api_user_reports.router, prefix="/user_reports")
router.include_router(api_world_data.router)
# router.include_router(auth.router, prefix="/auth")


################################################################################


@router.get("/")
@router.get("/{path:path}")
def page_not_found(path=""):
    return "Invalid Route", 404


@router.get("/ping")
def ping():
    return {"reply": "Hi!", "time": datetime.datetime.utcnow().isoformat()}


@router.get("/error")
def error():
    """Route to test error handling"""
    raise ValueError("something went wrong!")
