import json
from os import listdir
from os.path import join, basename
import sys

from getpass import getuser
from datetime import datetime
from typing import TextIO, Optional

from source.utils.task import Task
from source.utils.app_exeptions import TaskLimitError

class TaskJsonHandler:
    SOURCE_PATH = join("data")
    TASK_STATUS = {0: "todo", 1: "in_progress", 2: "done"}
    MAX_ITEM = 1e4

    def __init__(self) -> None:
        user_name = getuser()
        self.file_name = join(self.SOURCE_PATH, f"{user_name}'s_tasks.json")
        self.source_file = join(self.SOURCE_PATH, f"{user_name}'s_sources_for_app.json")
        self.__create_file()
    
    def __file_not_exists(self) -> bool:
        return not basename(self.file_name) in set(listdir(self.SOURCE_PATH))
    
    def __create_file(self) -> None:
        if self.__file_not_exists():
            obj = dict(todo = dict(), in_progress = dict(), done = dict())
            src_obj = dict(task_id = 0, del_task_id = [])
            with open(self.file_name, "w", encoding="utf-8") as file, open(self.source_file, "w", encoding="utf-8") as src_file:
                json.dump(obj, file, ensure_ascii=False, indent=4)
                json.dump(src_obj, src_file, ensure_ascii=False, indent=4)
    
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
    
    @staticmethod
    def _print_add_success(title: str, status: str, task_id: int) -> None:
        print(
            f"\033[1;32mTask successfully added!\033[0m\n\n"
            f"Task id: {task_id}\n"
            f"Task Title: {title}\n"
            f"Task Status: {status}\n\n"
            f"Use the \033[1m'list [--status]'\033[0m command to view all tasks."
        )
    
    @staticmethod
    def _print_update_success(description_flag: bool, title_flag: bool) -> None:
        print(
            f"\033[1;32mTask successfully updated!\033[0m\n\n"
            f"Title: {"updated" if title_flag else "not updated"}\n"
            f"Description: {"updated" if description_flag else "not updated"}\n\n"
            f"Use the \033[1m'list [--status]'\033[0m command to view all tasks."
        )
    
    @staticmethod
    def _print_delete_success(task_id: int) -> None:
        print(
            f"\033[1;32mThe task with id{task_id} has been successfully deleted!\033[0m\n"
        )
    
    @staticmethod
    def _print_mark_success(status: str) -> None:
        print(
            f"\033[1;32mThe task was successfully marked in the list as '{status}'!\033[0m"
        )
    
    
    def add(self, task_title: str, status: int = 0) -> None:
        with open(self.file_name, "r+", encoding="utf-8") as file, open(self.source_file, "r+", encoding="utf-8") as src_file:
            data = json.load(file)
            src_data = json.load(src_file)
            if src_data["task_id"] >= self.MAX_ITEM:
                raise TaskLimitError(int(self.MAX_ITEM))
            task = Task(task_title, status=status)

            if len(src_data["del_task_id"]) != 0:
                task_id = src_data["del_task_id"].pop()
            else:
                task_id = src_data["task_id"]
                src_data["task_id"] += 1
            print(task_id)
            data[self.TASK_STATUS[status]][task_id] = self.__date_to_str(task.__dict__)
            self.__dump_json(file, data)
            self.__dump_json(src_file, src_data)
            self._print_add_success(task_title, self.TASK_STATUS[status], int(task_id))
    
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
                description_flag = False
                title_flag = False
                if task_description is not None:
                    description_flag = True
                    task.description = task_description
                if task_title is not None:
                    title_flag = True
                    task.title = task_title
                task.updatedAt = datetime.now()
            data[self.TASK_STATUS[task.status]][task_id] = self.__date_to_str(task.__dict__)
            self.__dump_json(file, data)
            self._print_update_success(description_flag, title_flag)
    
    def delete(self, task_id: int) -> None:
        task_id = self.__check_id(task_id)
        with open(self.file_name, "r+", encoding="utf-8") as file, open(self.source_file, "r+", encoding="utf-8") as src_file:
            data = json.load(file)
            not_find_task = True
            for status in data:
                if task_id in data[status]:
                    src_data = json.load(src_file)
                    src_data["del_task_id"].append(task_id)
                    del data[status][task_id]
                    not_find_task = False
                    break
            if not_find_task:
                raise ValueError(f"The provided ID does not exist in the database.")

            self.__dump_json(file, data)
            self.__dump_json(src_file, src_data)
            self._print_delete_success(int(task_id))
    
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
            self._print_mark_success(self.TASK_STATUS[target_status])
    
    def mark_in_progress(self, task_id: int) -> None:
        self.__mark_task_status(task_id, 1)
    
    def mark_done(self, task_id: int) -> None:
        self.__mark_task_status(task_id, 2)
    
    def get_task_list(self, target_status: str = None) -> dict:
        with open(self.file_name, "r", encoding="utf-8") as file:
            data = json.load(file)
            if target_status is None:
                return data
            elif target_status in list(self.TASK_STATUS.values()):
                return data[target_status]
            raise ValueError("The status you are trying to retrieve does not exist.")

if __name__ == "__main__":
    data = [int(item) if item.isdigit() else item for item in sys.argv]
    task_handler = TaskJsonHandler()
    commands = {
        "add": (task_handler.add, 1, 2),
        "update": (task_handler.update, 2, 3),
        "delete": (task_handler.delete, 1, 1),
        "mark-in-progress": (task_handler.mark_in_progress, 1, 1),
        "mark-done": (task_handler.mark_done, 1, 1),
        "list": (task_handler.get_task_list, 0, 1),
        "update-title": (task_handler.update, 2, 2)
    }
    try:
        if data[1] in commands and len(data) - 2 in range(commands[data[1]][1],commands[data[1]][2]+1):
            if data[1] == list(commands.keys())[-1] and len(data) - 2 in range(commands[data[1]][1],commands[data[1]][2]+1):
                task_handler.update(data[2], task_title=data[3])
            else:
                result = commands[data[1]][0](*data[2:])
                if result:
                    print(result)
    except Exception as e:
        print(e)