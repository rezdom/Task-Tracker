import json
from datetime import datetime
import os

class TaskJsonHandler:
    SOURCE_PATH = "\..\Source"

    def __init__(self, file_name: str) -> None:
        self.file_name = file_name
    
    def __check_filename(self):
        return not self.file_name in set(os.listdir(self.SOURCE_PATH))
    
    def create_file(self):
        if self.__check_filename():
            obj = dict(in_progress = dict(), todo = dict(), complited = dict())
            with open(self.file_name, "w", encoding="utf-8") as file:
                json.dump(obj, file, ensure_ascii=False, indent=4)
    
    def add(self, task_title: str, task_description: str, date_time: datetime, mode: int = 0):
        with open(self.file_name) as file:
            data = json.load(file)

        if mode == 0:
            data["todo"][task_title] = {"title": task_title, "description": task_description, "date": date_time.strftime("%d/%m/%Y, %H:%M:%S")}
        elif mode == 1:
            data["in_progress"][task_title] = {"title": task_title, "description": task_description, "date": date_time.strftime("%d/%m/%Y, %H:%M:%S")}
        elif mode == 2:
            data["complited"][task_title] = {"title": task_title, "description": task_description, "date": date_time.strftime("%d/%m/%Y, %H:%M:%S")}
        
        with open(self.file_name, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)