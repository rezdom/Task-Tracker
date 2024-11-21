from source.json_handler import TaskJsonHandler
from source.utils.task import Task
from datetime import datetime

def welcome_msg() -> str:
    logo ="""
        ████████╗ █████╗ ███████╗██╗  ██╗     ████████╗██████╗  █████╗  ██████╗██╗  ██╗███████╗██████╗ 
        ╚══██╔══╝██╔══██╗██╔════╝██║ ██╔╝     ╚══██╔══╝██╔══██╗██╔══██╗██╔════╝██║ ██╔╝██╔════╝██╔══██╗
           ██║   ███████║███████╗█████╔╝         ██║   ██████╔╝███████║██║     █████╔╝ █████╗  ██████╔╝
           ██║   ██╔══██║╚════██║██╔═██╗         ██║   ██╔═██╗ ██╔══██║██║     ██╔═██╗ ██╔══╝  ██╔═██╗ 
           ██║   ██║  ██║███████║██║  ██╗        ██║   ██║  ██╗██║  ██║╚██████╗██║  ██╗███████╗██║  ██╗   
           ╚═╝   ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝        ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝   

    > Powered by RezDom...
    """
    return logo

def print_all_status(data: dict) -> None:
    module_separation = "=" * 32
    task_separation = "-" * 32
    print("\033[H\033[J")
    for status in data:
        print(f"\033[1m'{status}' tasks:\033[0m")
        if not data[status]:
            print(f"\nTasks not found\n")
            if not (status is list(data)[-1]):
                print(module_separation)
            continue
        for key, value in data[status].items():
            if not (key is list(data[status])[0]):
                print(task_separation)
            task = Task(
                value["title"],
                value["description"],
                datetime.strptime(value["createdAt"], "%d-%m-%Y, %H:%M:%S"),
                datetime.strptime(value["updatedAt"], "%d-%m-%Y, %H:%M:%S"),
                value["status"]
            )
            print(f"\n  ●id{key}\n{task}\n")
        if not (status is list(data)[-1]):
            print(module_separation)
    
def print_one_status(data:dict, target_status: str) -> None:
    task_separation = "-" * 32 
    print("\033[H\033[J")
    print(f"\033[1m'{target_status}' tasks:\033[0m\n")
    if not data:
        print(f"Tasks not found")
    for item in data:
        if not (item is list(data)[0]):
            print(task_separation)
        task = Task(
            data[item]["title"],
            data[item]["description"],
            datetime.strptime(data[item]["createdAt"], "%d-%m-%Y, %H:%M:%S"),
            datetime.strptime(data[item]["updatedAt"], "%d-%m-%Y, %H:%M:%S"),
            data[item]["status"]
        )
        print(f"\n  ●id{item}\n{task}\n")

if __name__ == "__main__":
    data = {
        "in_progress": {},
        "todo": {
            "0": {
                "title": "test1",
                "description": "no description jhdsfkdshfkj hskjfh sdhf kjdshfk jds fhdkj hfksjdf kjdsh kjhsdkjf hdsjk hfdsjkh fkdsjh fkjsdh fka",
                "createdAt": "20-11-2024, 16:23:14",
                "updatedAt": "20-11-2024, 16:23:14",
                "status": 0
            }
        },
        "done": {}
    }
    data_test = {
        "0": {
            "title": "test1",
            "description": "no description",
            "createdAt": "20-11-2024, 16:23:14",
            "updatedAt": "20-11-2024, 16:23:14",
            "status": 0
        }
    }
    print(welcome_msg())
    print_all_status(data)
    print("\n\n\n")
    print_one_status(data_test, "todo")