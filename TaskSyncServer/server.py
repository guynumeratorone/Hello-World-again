"""
Runs the TCP server for Task Sync Server.

The server listens for JSON requests from a client, validates each request,
calls the task manager logic, and sends a JSON response back to the client.
"""

import socket

from protocol import decode_message, encode_message, validate_request, create_response
from task_manager import (
    add_task,
    complete_task,
    delete_task,
    list_tasks,
    load_tasks,
    save_tasks
)


HOST = "127.0.0.1"
PORT = 5050
BUFFER_SIZE = 4096
TASK_FILE = "tasks.json"


def handle_request(request):
    """
    Process one decoded client request and return a response dictionary.
    """
    validation_result = validate_request(request)

    if not validation_result["success"]:
        return validation_result

    request_type = request["request_type"]
    tasks = load_tasks(TASK_FILE)

    if request_type == "server_status":
        return create_response(
            True,
            "Server is running.",
            {
                "server": "Task Sync Server",
                "task_count": len(tasks)
            }
        )

    if request_type == "add_task":
        task = request["task"]
        title = task.get("title", "")
        description = task.get("description", "")

        result = add_task(tasks, title, description)

        if result["success"]:
            save_tasks(tasks, TASK_FILE)

        return create_response(
            result["success"],
            result["message"],
            result.get("task")
        )

    if request_type == "list_tasks":
        result = list_tasks(tasks)

        return create_response(
            result["success"],
            result["message"],
            result.get("tasks")
        )

    if request_type == "complete_task":
        task_id = request["task_id"]
        result = complete_task(tasks, task_id)

        if result["success"]:
            save_tasks(tasks, TASK_FILE)

        return create_response(
            result["success"],
            result["message"],
            result.get("task")
        )

    if request_type == "delete_task":
        task_id = request["task_id"]
        result = delete_task(tasks, task_id)

        if result["success"]:
            save_tasks(tasks, TASK_FILE)

        return create_response(
            result["success"],
            result["message"],
            result.get("task")
        )

    return create_response(False, "Request could not be handled.")


def handle_client(client_socket, client_address):
    """
    Receive one client message, process it, and send one response.
    """
    print(f"Connected to client: {client_address}")

    try:
        received_data = client_socket.recv(BUFFER_SIZE).decode("utf-8")
        request = decode_message(received_data)

        if "success" in request and request["success"] is False:
            response = request
        else:
            response = handle_request(request)

        response_text = encode_message(response)
        client_socket.sendall(response_text.encode("utf-8"))

    except ConnectionError:
        error_response = create_response(False, "Connection error occurred.")
        client_socket.sendall(encode_message(error_response).encode("utf-8"))

    finally:
        client_socket.close()
        print(f"Disconnected from client: {client_address}")


def start_server(host=HOST, port=PORT):
    """
    Start the TCP server.
    """
    print("Starting Task Sync Server...")
    print(f"Listening on {host}:{port}")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((host, port))
        server_socket.listen()

        while True:
            client_socket, client_address = server_socket.accept()
            handle_client(client_socket, client_address)


if __name__ == "__main__":
    start_server()