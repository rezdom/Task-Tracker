import json
from os import listdir
from os.path import join, basename
import sys
from getpass import getuser
from datetime import datetime
from typing import TextIO

from utils.task import Task
from utils.app_exeptions import TaskLimitError

class TaskJsonHandler:
    SOURCE_PATH = join("..","data")
    TASK_STATUS = {0: "todo", 1: "in_progress", 2: "complited"}
    MAX_ITEM = 1e4

    def __init__(self) -> None:
        self.file_name = join(self.SOURCE_PATH, f"{getuser()}'s_tasks.json")
        self.__create_file()
    
    def __file_not_exists(self) -> bool:
        return not basename(self.file_name) in set(listdir(self.SOURCE_PATH))
    
    def __create_file(self) -> None:
        if self.__file_not_exists():
            obj = dict(in_progress = dict(), todo = dict(), complited = dict(), src = dict(task_id = 0, del_task_id = []))
            with open(self.file_name, "w", encoding="utf-8") as file:
                json.dump(obj, file, ensure_ascii=False, indent=4)
    
    @staticmethod
    def __date_to_str(data: dict) -> dict:
        for key in data:
            if key in ("createdAt", "updatedAt"):
                data[key] = data[key].strftime("%d-%m-%Y, %H:%M:%S")
        return data
    
    @staticmethod
    def __check_id(task_id: int) -> str:
        if not isinstance(task_id, int):
                raise TypeError(
                 f"The object is of type [{type(task_id).__name__}], "
                "but a [integer] object was expected."
            )
        return str(task_id)
    
    @staticmethod
    def __get_task_from_json(data: dict, task_id: str) -> dict:
        task = None
        for status in data:
            if task_id in data[status]:
                task = data[status][task_id]
                break
        if task is None:
            raise ValueError(f"The provided ID does not exist in the database.")
        return task
    
    @staticmethod
    def __dump_json(file: TextIO, data: dict) -> None:
        file.seek(0)
        json.dump(data, file, ensure_ascii=False, indent=4)
        #The file.truncate() clears remaining content in the file, 
        #preventing leftover data from being appended after updating the JSON.
        file.truncate()
    
    def add(self, task_title: str, status: int = 0) -> None:
        with open(self.file_name, "r+", encoding="utf-8") as file:
            data = json.load(file)
            if data["src"]["task_id"] >= self.MAX_ITEM:
                raise TaskLimitError(int(self.MAX_ITEM))
            task = Task(task_title, status=status)

            if len(data["src"]["del_task_id"]) != 0:
                data[self.TASK_STATUS[status]][data["src"]["del_task_id"].pop()] = self.__date_to_str(task.__dict__)
            else:
                data[self.TASK_STATUS[status]][data["src"]["task_id"]] = self.__date_to_str(task.__dict__)
                data["src"]["task_id"] += 1
            file.seek(0)
            json.dump(data, file, ensure_ascii=False, indent=4)
    
    def update(self, task_id: int, task_description: str = None, task_title: str = None) -> None:
        task_id = self.__check_id(task_id)
        with open(self.file_name, "r+", encoding="utf-8") as file:
            data = json.load(file)
            task = self.__get_task_from_json(data, task_id)
            task = Task(
                task["title"],
                task["description"],
                datetime.strptime(task["createdAt"], "%d-%m-%Y, %H:%M:%S"),
                datetime.strptime(task["updatedAt"], "%d-%m-%Y, %H:%M:%S"),
                task["status"]
            )

            if task_description is None and task_title is None:
                raise ValueError("Arguments were not provided.")
            else:
                if task_description is not None:
                    task.description = task_description
                if task_title is not None:
                    task.title = task_title
                task.updatedAt = datetime.now()
            data[self.TASK_STATUS[task.status]][task_id] = self.__date_to_str(task.__dict__)
            self.__dump_json(file, data)
    
    def delete(self, task_id: int) -> None:
        task_id = self.__check_id(task_id)
        with open(self.file_name, "r+", encoding="utf-8") as file:
            data = json.load(file)
            not_find_task = True
            for status in data:
                if task_id in data[status]:
                    data["src"]["del_task_id"].append(task_id)
                    del data[status][task_id]
                    not_find_task = False
                    break
            if not_find_task is None:
                raise ValueError(f"The provided ID does not exist in the database.")

            self.__dump_json(file, data)
    
    def __mark_task_status(self, task_id: int, target_status: int) -> None:
        task_id = self.__check_id(task_id)
        with open(self.file_name, "r+", encoding="utf-8") as file:
            data = json.load(file)
            task = None
            for status in data:
                if task_id in data[status]:
                    task = data[status][task_id]
                    del data[status][task_id]
                    break
            if task is None:
                raise ValueError(f"The provided ID does not exist in the database.")
            
            task = Task(
                task["title"],
                task["description"],
                datetime.strptime(task["createdAt"], "%d-%m-%Y, %H:%M:%S"),
                datetime.strptime(task["updatedAt"], "%d-%m-%Y, %H:%M:%S"),
                task["status"]
            )
            task.status = target_status
            task.updatedAt = datetime.now()
            data[self.TASK_STATUS[task.status]][task_id] = self.__date_to_str(task.__dict__)

            self.__dump_json(file, data)
    
    def mark_in_progress(self, task_id: int) -> None:
        self.__mark_task_status(task_id, 1)
    
    def mark_done(self, task_id: int) -> None:
        self.__mark_task_status(task_id, 2)

if __name__ == "__main__":
    data = [int(item) if item.isdigit() else item for item in sys.argv]
    task_handler = TaskJsonHandler()
    commands = {
        "add": (task_handler.add, 1, 2),
        "update": (task_handler.update, 2, 3),
        "delete": (task_handler.delete, 1, 1),
        "mark-in-progress": (task_handler.mark_in_progress, 1, 1),
        "mark-done": (task_handler.mark_done, 1, 1),
        "update-title": (task_handler.update, 2, 2)
    }
    try:
        if data[1] in commands and len(data) - 2 in range(commands[data[1]][1],commands[data[1]][2]+1):
            if data[1] == list(commands.keys())[-1] and len(data) - 2 in range(commands[data[1]][1],commands[data[1]][2]+1):
                task_handler.update(data[2], task_title=data[3])
            else:
                commands[data[1]][0](*data[2:])
    except Exception as e:
        print(e)