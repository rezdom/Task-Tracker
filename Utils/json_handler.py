import json
from datetime import datetime
from os import listdir
from os.path import join, basename
import sys
from getpass import getuser

class Task:
    def __init__(self, task_title: str, task_description: str = "no description", crtime: datetime = datetime.now(), uptime: datetime = datetime.now(), status: int = 0) -> None:
        self.title = task_title
        self.description = task_description
        self.createdAt = crtime.strftime("%d-%m-%Y, %H:%M:%S")
        self.updatedAt = uptime.strftime("%d-%m-%Y, %H:%M:%S")
        self.status = status


class TaskJsonHandler:
    SOURCE_PATH = join("..","Source")
    TASK_STATUS = {0: "todo", 1: "in_progress", 2: "comlited"}
    MAX_ITEM = 1e5

    def __init__(self) -> None:
        self.file_name = join(self.SOURCE_PATH, f"task_of_{getuser()}.json")
        self.__create_file()
    
    def __is_file_exists(self) -> bool:
        return not basename(self.file_name) in set(listdir(self.SOURCE_PATH))
    
    def __create_file(self) -> None:
        if self.__is_file_exists():
            obj = dict(in_progress = dict(), todo = dict(), complited = dict(), src = dict(task_id = 0))
            with open(self.file_name, "w", encoding="utf-8") as file:
                json.dump(obj, file, ensure_ascii=False, indent=4)
    
    def add(self, task_title: str, status: int = 0):
        with open(self.file_name) as file:
            data = json.load(file)
        task = Task(task_title, status=status)
        if status in self.TASK_STATUS and data["src"]["task_id"] < self.MAX_ITEM:
            data[self.TASK_STATUS[status]][data["src"]["task_id"]] = task.__dict__
            data["src"]["task_id"] += 1
        
        with open(self.file_name, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    data = sys.argv
    task_handler = TaskJsonHandler()
    commands = {
        "add": (task_handler.add, 1)
    }
    if data[1] in commands and len(data) - 2 == commands[data[1]][1]:
        commands[data[1]][0](*data[2:])