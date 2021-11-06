# google-api-python-client

# google-cloud-tasks==2.2.0
import os
import json
import urllib
from google.cloud import tasks_v2

from lorgs import data

PWD = os.path.dirname(__file__)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.abspath(f"{PWD}/../google_creds.json")


TASK_CLIENT = tasks_v2.CloudTasksClient()
TASK_QUEUE = "projects/lorrgs/locations/europe-west2/queues/lorgs-task-queue"


# project = "lorrgs"
# location = "europe-west2"
# parent = f"projects/{project}/locations/{location}"
# queue = "lorgs-task-queue"
# parent = client.queue_path(project, location, queue)
# print("parent", parent)

import uuid


def build_task_name(name):
    return f"{TASK_QUEUE}/tasks/{name}"



def create_task(url, name, limit=None):
    # print(boss)
    if limit:
        url += f"?limit={limit}"

    name = build_task_name(f"{name}.{uuid.uuid4()}")
    task = {
        "name": name,
        "app_engine_http_request": {  # Specify the type of request.
            "http_method": tasks_v2.HttpMethod.GET,
            "relative_uri": url
        }
    }
    return TASK_CLIENT.create_task(request={"parent": TASK_QUEUE, "task": task})


def create_test_task():

    task = create_task("/api/ping", "ping")
    print(task)
    print("NAME:", task.name)




def test_tasks():


    url_base = "https://europe-west1-lorrgs.cloudfunctions.net"
    func_name = "load_spec_rankings"

    params = {
        "boss_slug": data.GUARDIAN.full_name_slug,
        "spec_slug": "",
        "limit": 12,
    }

    url = f"{url_base}/{func_name}"
    if params:
        url += "?" + urllib.parse.urlencode(params)
    print("url", url)


    task = {
        "http_request": {  # Specify the type of request.
            "http_method": tasks_v2.HttpMethod.GET,
            "url": url,
        }
    }
    print("task", task)
    client.create_task(request={"parent": parent, "task": task})


def list_tasks():
    tasks = TASK_CLIENT.list_tasks(parent=TASK_QUEUE)
    for task in tasks:
        print("Task:", task.name)


def get_task_status():

    from google.api_core.exceptions import NotFound


    name = "ping-5bdc3a4b-59f2-43f2-ac6c-cf3e83efb792"
    name = "user_report_load__de29ebc6-fbd1-4ac4-9cb6-c1ebfe292a7d"
    full_name = build_task_name(name)

    try:
        task = TASK_CLIENT.get_task(name=full_name)
    except NotFound:
        print("done")
    else:
        print("task", task)


# from aiogoogle.auth.creds import ServiceAccountCreds
# creds = ServiceAccountCreds(
#     scopes=[
#         "https://www.googleapis.com/auth/devstorage.read_only",
#         "https://www.googleapis.com/auth/devstorage.read_write",
#         "https://www.googleapis.com/auth/devstorage.full_control",
#         "https://www.googleapis.com/auth/cloud-platform.read-only",
#         "https://www.googleapis.com/auth/cloud-platform",
#     ],
# )
