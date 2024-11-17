import json
from os import listdir
from os.path import join, basename
import sys
from getpass import getuser

from utils.task import Task
from utils.app_exeptions import TaskLimitError

class TaskJsonHandler:
    SOURCE_PATH = join("..","data")
    TASK_STATUS = {0: "todo", 1: "in_progress", 2: "comlited"}
    MAX_ITEM = 1e5

    def __init__(self) -> None:
        self.file_name = join(self.SOURCE_PATH, f"task_of_{getuser()}.json")
        self.__create_file()
    
    def __file_not_exists(self) -> bool:
        return not basename(self.file_name) in set(listdir(self.SOURCE_PATH))
    
    def __create_file(self) -> None:
        if self.__file_not_exists():
            obj = dict(in_progress = dict(), todo = dict(), complited = dict(), src = dict(task_id = 0))
            with open(self.file_name, "w", encoding="utf-8") as file:
                json.dump(obj, file, ensure_ascii=False, indent=4)
    
    @staticmethod
    def __date_to_str(data: dict) -> dict:
        for key in data:
            if key in ("createdAt", "updatedAt"):
                data[key] = data[key].strftime("%d-%m-%Y, %H:%M:%S")
        return data
    
    def add(self, task_title: str, status: int = 0) -> None:
        with open(self.file_name, "r+", encoding="utf-8") as file:
            data = json.load(file)
            if data["src"]["task_id"] >= self.MAX_ITEM:
                raise TaskLimitError(int(self.MAX_ITEM))
            task = Task(task_title, status=status)
            data[self.TASK_STATUS[status]][data["src"]["task_id"]] = self.__date_to_str(task.__dict__)
            data["src"]["task_id"] += 1
            file.seek(0)
            json.dump(data, file, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    data = sys.argv
    task_handler = TaskJsonHandler()
    commands = {
        "add": (task_handler.add, 1)
    }
    if data[1] in commands and len(data) - 2 == commands[data[1]][1]:
        commands[data[1]][0](*data[2:])