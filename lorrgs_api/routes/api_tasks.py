"""Get Information about Tasks."""
# IMPORT THIRD PARTY LIBRARIES
import fastapi

# IMPORT LOCAL LIBRARIES
from lorgs.models.task import Task

router = fastapi.APIRouter(tags=["tasks"], prefix="/tasks")


################################################################################
# Task Status
#
@router.get("/{task_id}")
async def get_task(response: fastapi.Response, task_id):
    response.headers["Cache-Control"] = "no-cache"

    task = Task.get(key=task_id)
    if not task:
        return "Task not found.", 404

    return {
        "task_id": task.key,
        "status": task.status,
        "message": task.message,
        "updated": task.updated.isoformat(),
        "items": task.items,
    }
