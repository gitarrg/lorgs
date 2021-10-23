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


from aiogoogle import Aiogoogle


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


# async def create_gogole_client(name, version):
#     async with Aiogoogle() as aiogoogle:
#         # Downloads the API specs and creates an API object
#         return await aiogoogle.discover(name, version)
# 
# async def create_task_client():
#     return await create_gogole_client("cloudtasks", "v2")
from aiogoogle.auth.creds import ServiceAccountCreds

service_account_key = json.load(open("./google_creds.json"))
# print("service_account_key", service_account_key)

creds = ServiceAccountCreds(
    scopes=["https://www.googleapis.com/auth/cloud-tasks"],
    **service_account_key
)


async def async_google_test():

    TASK_QUEUE = "projects/lorrgs/locations/europe-west2/queues/lorgs-task-queue"

    task_name = "user_report_load__8fb1d213-4632-40b7-a577-b6713052a488"
    task_path = f"{TASK_QUEUE}/tasks/{task_name}"

    async with Aiogoogle(service_account_creds=creds) as aiogoogle:
        task_client = await aiogoogle.discover("cloudtasks", "v2")

        res = await aiogoogle.as_service_account(
            # task_client.projects.locations.list(name="projects/lorrgs")
            task_client.projects.locations.queues.tasks.get(name=task_path)
        )
        print(res)

    # https://cloud.google.com/tasks/docs/reference/rest/v2/projects.locations.queues.tasks/list



if __name__ == '__main__':
    # load_all()
    # create_test_task()
    # get_task_status()

    import asyncio

    asyncio.run(async_google_test())

    # from google.cloud import tasks_v2
    # print(tasks_v2)
