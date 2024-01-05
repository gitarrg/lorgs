from lorgs.models.task import Task


def test_create_task():
    task = Task(
        task_id="debug1",
    )
    task.save()


def test_get_task():
    task = Task.get(task_id="debug1")
    print(task)


if __name__ == "__main__":
    test_create_task()
    # test_get_task()
