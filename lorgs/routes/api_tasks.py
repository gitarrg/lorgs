"""Utils to create Scheduled Tasks

These are primarily used in the cron jobs to periodically update the data.

"""
# IMPORT STANDARD LIBRARIES
import os
import urllib
import uuid

# IMPORT THIRD PARTY LIBRARIES
from google.api_core.exceptions import NotFound
from google.cloud import tasks_v2
import fastapi

# IMPORT LOCAL LIBRARIES
from lorgs import utils


CLOUD_FUNCTIONS_ROOT = os.getenv("CLOUD_FUNCTIONS_ROOT") or "https://europe-west1-lorrgs.cloudfunctions.net"
TASK_QUEUE = "projects/lorrgs/locations/europe-west2/queues/lorgs-task-queue"

# Google Cloud Tasks Client Instance
TASK_CLIENT = tasks_v2.CloudTasksClient()


router = fastapi.APIRouter(tags=["tasks"])


def get_task_full_name(name):
    """Create a fully qualified task name (or rather task path)."""
    return f"{TASK_QUEUE}/tasks/{name}"


################################################################################
# Task Status
#
@utils.run_in_executor
def _get_task(task_id):
    full_name = get_task_full_name(task_id)
    return TASK_CLIENT.get_task(name=full_name)


@router.get("/{task_id}")
async def get_task(task_id: str):
    """Get a single task by ID."""
    try:
        await _get_task(task_id)
    except NotFound:
        # could be an invalid task id, or completed...
        # all we know is that its not in the queue
        return {"status": "not found"}
    else:
        return {"status": "pending"}


################################################################################
# Google Tasks
#
@utils.run_in_executor
def submit_task(task):
    """Submit a task to the queue"""
    return TASK_CLIENT.create_task(request={"parent": TASK_QUEUE, "task": task})


async def create_cloud_function_task(function_name, **kwargs):
    """Creates an Task, that will execute a Cloud Function.

    Args:
        function_name (str): name of the function to run
    """

    task_uuid = uuid.uuid4()
    task_name = f"{function_name}__{task_uuid}"
    full_name = get_task_full_name(task_name)

    url = f"{CLOUD_FUNCTIONS_ROOT}/{function_name}"
    if kwargs:
        url += "?" + urllib.parse.urlencode(kwargs)

    await submit_task({
        "name": full_name,
        "http_request": {  # Specify the type of request.
            "http_method": tasks_v2.HttpMethod.GET,
            "url": url,
        }
    })

    return task_name


async def create_app_engine_task(url, **kwargs):
    """Creates a task that will call an app engine endpoint.

    Args:
        url (str): the url to call

    """
    if kwargs:
        url += "?" + urllib.parse.urlencode(kwargs)

    task = {
        "app_engine_http_request": {  # Specify the type of request.
            "http_method": tasks_v2.HttpMethod.GET,
            "relative_uri": url
        }
    }
    return await submit_task(task)
