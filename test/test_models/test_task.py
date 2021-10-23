

# IMPORT THIRD PARTY LIBRARIES
import dotenv
dotenv.load_dotenv() # pylint: disable=wrong-import-position

# IMPORT LOCAL LIBRARIES
from lorgs import db  # pylint: disable=unused-import
from lorgs.models.task import Task




def create_task():
    task = Task()
    print(task.id)
    task.save()
    print(task.id)


def update_task_status():

    task_id = "12313cbedd812-5c16-4a89-a1c7-db4022f24c55"
    task = Task.objects.get(id=task_id)
    print("task", task)
    task.status = Task.STATUS_PENDING
    print(task)
    print(task.as_dict())
    task.save()



if __name__ == "__main__":
    # create_task()
    update_task_status()
