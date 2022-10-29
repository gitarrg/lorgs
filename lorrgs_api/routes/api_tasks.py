"""Get Information about Tasks."""
# IMPORT THIRD PARTY LIBRARIES
import fastapi

# IMPORT LOCAL LIBRARIES
from lorgs.models.task import Task

router = fastapi.APIRouter(tags=["tasks"])


################################################################################
# Task Status
#
@router.get("/{task_id}")
async def get_task(response: fastapi.Response, task_id):

    task = Task.from_id(task_id=task_id)
    if not task:
        return "Task not found.", 404

    response.headers["Cache-Control"] = "no-cache"
    return {
        "task_id": task.task_id,
        "status": task.status,
        "message": task.message,
        "updated": int(task.updated.timestamp()),
    }
