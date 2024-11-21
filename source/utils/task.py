import source.utils.task_descriptors as td
from datetime import datetime
import textwrap

class Task:
    createdAt = td.DateValidator()
    updatedAt = td.DateValidator()
    status = td.StatusValidator()
    description = td.DescriptorValidator()
    title = td.TitleValidator()

    def __init__(self, task_title: str, task_description: str = "no description", crtime: datetime = datetime.now(),
                 uptime: datetime = datetime.now(), status: int = 0) -> None:
        self.title = task_title
        self.description = task_description
        self.createdAt = crtime
        self.updatedAt = uptime
        self.status = status
    
    def __str__(self) -> str:
        max_description_length = 64
        wrapped_description = '\n'.join(f"\t{line}" for line in textwrap.fill(self.description, max_description_length).splitlines())
        task_status = "todo" if self.status == 0 else "in_progress" if self.status == 1 else "done"
        return (
    f"""    - Title of task: {self.title}
    - Description of task:\n{wrapped_description}
    - Status: {task_status}
    - Last update time: {self.updatedAt}
    - Created at: {self.createdAt}"""
        )