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
    f"""    \033[1;32m- Title of task:\033[0m {self.title}
    \033[1;32m- Description of task:\033[0m\n{wrapped_description}
    \033[1;32m- Status:\033[0m {task_status}
    \033[1;32m- Last update time:\033[0m {self.updatedAt}
    \033[1;32m- Created at:\033[0m {self.createdAt}"""
        )