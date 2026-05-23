"""
Handles the core task-management logic for Task Sync Server.
"""

import json
import os


DEFAULT_TASK_FILE = "tasks.json"


def load_tasks(file_path=DEFAULT_TASK_FILE):
    """
    Load tasks from a JSON file.

    If the file does not exist or is empty, return an empty list.
    """
    if not os.path.exists(file_path):
        return []

    if os.path.getsize(file_path) == 0:
        return []

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            tasks = json.load(file)

        if isinstance(tasks, list):
            return tasks

        return []

    except json.JSONDecodeError:
        return []


def save_tasks(tasks, file_path=DEFAULT_TASK_FILE):
    """
    Save the task list to a JSON file.
    """
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(tasks, file, indent=4)

    return {
        "success": True,
        "message": "Tasks saved successfully."
    }


def get_next_task_id(tasks):
    """
    Find the next available task ID.
    """
    if not tasks:
        return 1

    highest_id = 0

    for task in tasks:
        task_id = task.get("id", 0)

        if isinstance(task_id, int) and task_id > highest_id:
            highest_id = task_id

    return highest_id + 1


def add_task(tasks, title, description=""):
    """
    Add a new task to the task list.
    """
    if not title or not title.strip():
        return {
            "success": False,
            "message": "Task title cannot be empty.",
            "task": None
        }

    new_task = {
        "id": get_next_task_id(tasks),
        "title": title.strip(),
        "description": description.strip(),
        "completed": False
    }

    tasks.append(new_task)

    return {
        "success": True,
        "message": "Task added successfully.",
        "task": new_task
    }


def list_tasks(tasks):
    """
    Return all tasks.
    """
    return {
        "success": True,
        "message": "Tasks retrieved successfully.",
        "tasks": tasks
    }


def complete_task(tasks, task_id):
    """
    Mark a task as complete by ID.
    """
    for task in tasks:
        if task.get("id") == task_id:
            task["completed"] = True

            return {
                "success": True,
                "message": "Task completed successfully.",
                "task": task
            }

    return {
        "success": False,
        "message": f"No task found with ID {task_id}.",
        "task": None
    }


def delete_task(tasks, task_id):
    """
    Delete a task by ID.
    """
    for task in tasks:
        if task.get("id") == task_id:
            tasks.remove(task)

            return {
                "success": True,
                "message": "Task deleted successfully.",
                "task": task
            }

    return {
        "success": False,
        "message": f"No task found with ID {task_id}.",
        "task": None
    }