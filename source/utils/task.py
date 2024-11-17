import utils.task_descriptors as td
from datetime import datetime

class Task:
    createdAt = td.DateValidator()
    updatedAt = td.DateValidator()

    def __init__(self, task_title: str, task_description: str = "no description", crtime: datetime = datetime.now(),
                 uptime: datetime = datetime.now(), status: int = 0) -> None:
        self.title = task_title
        self.description = task_description
        self.createdAt = crtime
        self.updatedAt = uptime
        self.status = status