"""Utils to create Scheduled Tasks

These are primarily used in the cron jobs to periodically update the data.

"""

# IMPORT STANDARD LIBRARIES
import urllib

# IMPORT THIRD PARTY LIBRARIES
import flask
from google.cloud import tasks_v2


def create_task(url):
    google_task_client = tasks_v2.CloudTasksClient()
    parent = "projects/lorrgs/locations/europe-west2/queues/lorgs-task-queue"

    if flask.request.args:
        url += "?" + urllib.parse.urlencode(flask.request.args)

    task = {
        "app_engine_http_request": {  # Specify the type of request.
            "http_method": tasks_v2.HttpMethod.GET,
            "relative_uri": url
        }
    }

    if flask.current_app.config["LORRGS_DEBUG"]:
        print("create_task", url)
        return

    return google_task_client.create_task(request={"parent": parent, "task": task})
