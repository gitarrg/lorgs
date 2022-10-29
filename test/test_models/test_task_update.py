"""Test"""

import dotenv
dotenv.load_dotenv()

from lorgs import db
from lorgs.models.task import Task


TASK_ID = "63514952-6a3e-4a47-8d95-8be1596c407f"

task = Task.update_task(TASK_ID, status="done")


