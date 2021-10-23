"""Utils to create Scheduled Tasks

These are primarily used in the cron jobs to periodically update the data.

"""

# IMPORT STANDARD LIBRARIES
import os
import urllib
import uuid

# IMPORT THIRD PARTY LIBRARIES
from google.cloud import tasks_v2
from google.api_core.exceptions import NotFound
import flask
import mongoengine as me

# IMPORT LOCAL LIBRARIES
from lorgs.models.task import Task


CLOUD_FUNCTIONS_ROOT = os.getenv("CLOUD_FUNCTIONS_ROOT") or "https://europe-west1-lorrgs.cloudfunctions.net"
TASK_QUEUE = "projects/lorrgs/locations/europe-west2/queues/lorgs-task-queue"


blueprint = flask.Blueprint("api.tasks", __name__)


def get_google_task_client():
    return tasks_v2.CloudTasksClient()


def get_task_full_name(name):
    return f"{TASK_QUEUE}/tasks/{name}"


################################################################################
# Task Status
#

@blueprint.route("/")
def get_tasks():
    """List all Tasks."""
    return {str(task.id): task.as_dict() for task in Task.objects} # pylint: disable=no-member


@blueprint.route("/<string:task_id>")
def get_task(task_id):
    """Get a single task by ID."""
    try:
        task = Task.objects.get(id=task_id) # pylint: disable=no-member
    except me.DoesNotExist:
        return "invalid task id", 404
    else:
        return task.as_dict()


################################################################################
# Google Tasks
#
def submit_task(task):

    if flask.current_app.config["LORRGS_DEBUG"]:
        print("submit_task", task)
        return

    google_task_client = tasks_v2.CloudTasksClient()
    return google_task_client.create_task(request={"parent": TASK_QUEUE, "task": task})



def create_cloud_function_task(function_name, **kwargs):
    """Creates an Task, that will execute a Cloud Function.

    Args:
        function_name (str): name of the function to run
    """

    task_uuid = uuid.uuid4()
    full_name = f"{TASK_QUEUE}/tasks/{function_name}__{task_uuid}"

    url = f"{CLOUD_FUNCTIONS_ROOT}/{function_name}"
    if kwargs:
        url += "?" + urllib.parse.urlencode(kwargs)

    submit_task({
        "name": full_name,
        "http_request": {  # Specify the type of request.
            "http_method": tasks_v2.HttpMethod.GET,
            "url": url,
        }
    })

    return task_uuid


def create_app_engine_task(url, **kwargs):
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
    return submit_task(task)
