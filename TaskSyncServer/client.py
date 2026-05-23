"""
Runs the command-line client for Task Sync Server.

The client displays a simple numbered menu, creates JSON requests based on
the user's choices, sends those requests to the TCP server, and displays the
server's response.
"""

import socket

from protocol import decode_message, encode_message


HOST = "127.0.0.1"
PORT = 5050
BUFFER_SIZE = 4096


def send_request(request, host=HOST, port=PORT):
    """
    Send one request to the server and return the decoded response.
    """
    try:
        request_text = encode_message(request)

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((host, port))
            client_socket.sendall(request_text.encode("utf-8"))

            response_text = client_socket.recv(BUFFER_SIZE).decode("utf-8")
            return decode_message(response_text)

    except ConnectionRefusedError:
        return {
            "success": False,
            "message": "Could not connect to server. Make sure server.py is running.",
            "data": None
        }

    except ConnectionError:
        return {
            "success": False,
            "message": "A connection error occurred.",
            "data": None
        }


def display_response(response):
    """
    Display a server response in a readable way.
    """
    print()
    print("Server Response")
    print("---------------")
    print(f"Success: {response.get('success')}")
    print(f"Message: {response.get('message')}")

    data = response.get("data")

    if isinstance(data, list):
        if not data:
            print("Tasks: No tasks found.")
        else:
            print("Tasks:")

            for task in data:
                status = "Complete" if task.get("completed") else "Incomplete"
                print(f"  ID: {task.get('id')}")
                print(f"  Title: {task.get('title')}")
                print(f"  Description: {task.get('description')}")
                print(f"  Status: {status}")
                print()

    elif isinstance(data, dict):
        print("Data:")

        for key, value in data.items():
            print(f"  {key}: {value}")

    elif data is not None:
        print(f"Data: {data}")

    print()


def prompt_for_task_id():
    """
    Ask the user for a task ID and validate that it is an integer.
    """
    task_id_text = input("Enter task ID: ").strip()

    try:
        return int(task_id_text)

    except ValueError:
        print("Task ID must be a number.")
        return None


def create_add_task_request():
    """
    Prompt the user for task information and create an add_task request.
    """
    title = input("Enter task title: ").strip()
    description = input("Enter task description: ").strip()

    return {
        "request_type": "add_task",
        "task": {
            "title": title,
            "description": description
        }
    }


def create_complete_task_request():
    """
    Prompt the user for a task ID and create a complete_task request.
    """
    task_id = prompt_for_task_id()

    if task_id is None:
        return None

    return {
        "request_type": "complete_task",
        "task_id": task_id
    }


def create_delete_task_request():
    """
    Prompt the user for a task ID and create a delete_task request.
    """
    task_id = prompt_for_task_id()

    if task_id is None:
        return None

    return {
        "request_type": "delete_task",
        "task_id": task_id
    }


def display_menu():
    """
    Display the client menu.
    """
    print("Task Sync Client")
    print("----------------")
    print("1. Check server status")
    print("2. Add task")
    print("3. List tasks")
    print("4. Complete task")
    print("5. Delete task")
    print("6. Exit")


def run_client():
    """
    Run the client menu loop.
    """
    while True:
        display_menu()
        choice = input("Choose an option: ").strip()

        request = None

        if choice == "1":
            request = {
                "request_type": "server_status"
            }

        elif choice == "2":
            request = create_add_task_request()

        elif choice == "3":
            request = {
                "request_type": "list_tasks"
            }

        elif choice == "4":
            request = create_complete_task_request()

        elif choice == "5":
            request = create_delete_task_request()

        elif choice == "6":
            print("Exiting Task Sync Client.")
            break

        else:
            print("Invalid menu option.")
            print()

        if request is not None:
            response = send_request(request)
            display_response(response)


if __name__ == "__main__":
    run_client()