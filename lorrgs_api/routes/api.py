"""Endpoints related to the Backend/API."""

# IMPORT STANDARD LIBRARIES
import datetime

# IMPORT THIRD PARTY LIBRARIES
import fastapi

# IMPORT LOCAL LIBRARIES
from lorrgs_api.routes import api_comp_rankings
from lorrgs_api.routes import api_spec_rankings
from lorrgs_api.routes import api_tasks
from lorrgs_api.routes import api_user_reports
from lorrgs_api.routes import api_world_data
# from lorgs.routes import auth


router = fastapi.APIRouter()


################################################################################
# Child Blueprints
router.include_router(api_comp_rankings.router)
router.include_router(api_spec_rankings.router)
router.include_router(api_tasks.router, prefix="/tasks")
router.include_router(api_user_reports.router, prefix="/user_reports")
router.include_router(api_world_data.router)
# router.include_router(auth.router, prefix="/auth")


################################################################################


@router.get("/ping")
def ping():
    return {"reply": "Hi!", "time": datetime.datetime.utcnow().isoformat()}


@router.get("/ping_dc")
def ping_dc(response: fastapi.Response):

    ts = datetime.datetime.utcnow().isoformat()
    payload = {"Text": "Hello", "time": ts}

    from lorgs.models.task import Task
    task = Task.submit("discord", payload)
    payload["id"] = task.task_id

    response.headers["Cache-Control"] = "no-cache"
    return payload


@router.get("/error")
def error():
    """Route to test error handling"""
    raise ValueError("something went wrong!")


@router.get("/")
@router.get("/{path:path}")
def page_not_found(path=""):
    return "Invalid Route", 404
