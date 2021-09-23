# google-api-python-client

# google-cloud-tasks==2.2.0
import os
from google.cloud import tasks_v2

from lorgs import data

PWD = os.path.dirname(__file__)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.abspath(f"{PWD}/../google_creds.json")


client = tasks_v2.CloudTasksClient()

# project = "lorrgs"
# location = "europe-west2"
# parent = f"projects/{project}/locations/{location}"
# queue = "lorgs-task-queue"
# parent = client.queue_path(project, location, queue)
# print("parent", parent)
parent = "projects/lorrgs/locations/europe-west2/queues/lorgs-task-queue"


def create_task(url, limit=None):
    # print(boss)
    if limit:
        url += f"?limit={limit}"

    task = {
        "app_engine_http_request": {  # Specify the type of request.
            "http_method": tasks_v2.HttpMethod.GET,
            "relative_uri": url
        }
    }
    return client.create_task(request={"parent": parent, "task": task})



def load_all():
    for boss in data.SANCTUM_OF_DOMINATION_BOSSES:
        for spec in data.SUPPORTED_SPECS:
            print(spec, "vs", boss)

            url = f"/api/load_spec_rankings/{spec.full_name_slug}/{boss.name_slug}"
            create_task(url)

    comp_name = "any-heal"
    for boss in data.SANCTUM_OF_DOMINATION_BOSSES:
        print(comp_name, "vs", boss)
        url = f"/api/load_comp_ranking/{comp_name}/{boss.name_slug}"
        create_task(url, limit=20)



def test_tasks():

    for i in range(200):
        task = {
            "app_engine_http_request": {  # Specify the type of request.
                "http_method": tasks_v2.HttpMethod.GET,
                "relative_uri": f"/api/async_test/{i}"
            }
        }
        client.create_task(request={"parent": parent, "task": task})


if __name__ == '__main__':
    # load_all()
    # test_tasks()

    # from google.cloud import tasks_v2
    print(tasks_v2)
