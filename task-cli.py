from argparse import ArgumentParser, SUPPRESS, RawTextHelpFormatter
import sys
from pprint import pprint
pprint(sys.path)
from source.json_handler import TaskJsonHandler
from source.display_for_task import welcome_msg, print_all_status, print_one_status


def get_arg_parser() -> ArgumentParser:
    parser = ArgumentParser(description=f"\033[H\033[J{welcome_msg()}",formatter_class=RawTextHelpFormatter, usage=SUPPRESS)

    subparsers = parser.add_subparsers(dest="command", required=True, help="Commands for work on tasks")

    add_parser = subparsers.add_parser("add", help="Create a task, by default in 'todo' list")
    add_parser.add_argument("task_title", type=str, help='Title of the task, entered in quotes. From 4 to 64 characters ("For example").')
    add_parser.add_argument("--status", "-s", type=int, help='Set status. 0 - todo, 1-in_progress, 2 - done. Optional argument.')

    update_parser = subparsers.add_parser("update", help="Updating the description and title of an existing task by its id.")
    update_parser.add_argument("task_id", type=int, help="The ID of the targeted task")
    update_parser.add_argument("task_description", type=str, help="New description for task (from 16 to 2048 characters). By default, the task has no description.")
    update_parser.add_argument("--title", "-t", type=str, help="New title for task (from 4 to 64 characters)")

    update_title_parser = subparsers.add_parser("update-title", help="Updating only title of an existing task by its id.")
    update_title_parser.add_argument("task_id", type=int, help="The ID of the targeted task")
    update_title_parser.add_argument("title", type=str, help="New title for task (from 4 to 64 characters)")

    delete_parser = subparsers.add_parser("delete", help="Deleting tasks from database through task's id")
    delete_parser.add_argument("id", type=int, help="The ID of the targeted task")

    mark_in_progress_parser = subparsers.add_parser("mark-in-progress", help="Setting the task to the 'in-progress' state")
    mark_in_progress_parser.add_argument("task_id", type=int, help="The ID of the targeted task")

    mark_done_parser = subparsers.add_parser("mark-done", help="Setting the task to the 'done' state")
    mark_done_parser.add_argument("task_id", type=int, help="The ID of the targeted task")

    list_parser = subparsers.add_parser("list", help="Displaying a list of tasks")
    list_parser.add_argument("-s", "--status", type=str, help="Select a specific task status to display ('todo', 'in_progress', 'done')")

    return parser

def main():
    args = get_arg_parser().parse_args()
    args_value_list = [item for item in list(vars(args).values()) if item is not None]

    task_handler = TaskJsonHandler()
    commands = {
        "add": task_handler.add,
        "update": task_handler.update,
        "delete": task_handler.delete,
        "mark-in-progress": task_handler.mark_in_progress,
        "mark-done": task_handler.mark_done,
        "list": task_handler.get_task_list,
        "update-title": task_handler.update
    }

    try:
        if args_value_list[0] in commands:
            if args_value_list[0] == list(commands)[-1]:
                task_handler.update(args_value_list[1], task_title=args_value_list[2])
            elif args_value_list[0] == list(commands)[-2]:
                data = commands[args_value_list[0]](list(vars(args).values())[1])
                if set(data) == set(task_handler.TASK_STATUS.values()):
                    print_all_status(data)
                else:
                    print_one_status(data, args_value_list[1])
            else:
                commands[args_value_list[0]](*args_value_list[1:])
    except Exception as e:
        print(f"\n\033[31m{e}\033[0m")

if __name__ == "__main__":
    main()