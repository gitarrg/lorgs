"""Utils to create Scheduled Tasks

These are primarily used in the cron jobs to periodically update the data.

"""

# IMPORT STANDARD LIBRARIES
import os
import urllib

# IMPORT THIRD PARTY LIBRARIES
import flask
from google.cloud import tasks_v2


CLOUD_FUNCTIONS_ROOT = os.getenv("CLOUD_FUNCTIONS_ROOT") or "https://europe-west1-lorrgs.cloudfunctions.net"
TASK_QUEUE = "projects/lorrgs/locations/europe-west2/queues/lorgs-task-queue"


###############################

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
    url = f"{CLOUD_FUNCTIONS_ROOT}/{function_name}"

    if kwargs:
        url += "?" + urllib.parse.urlencode(kwargs)

    task = {
        "http_request": {  # Specify the type of request.
            "http_method": tasks_v2.HttpMethod.GET,
            "url": url,
        }
    }
    return submit_task(task)



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
