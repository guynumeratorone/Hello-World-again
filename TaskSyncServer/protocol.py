"""
Handles JSON request validation and response formatting for Task Sync Server.

The client and server both use this structure so they can communicate using
consistent request and response messages.
"""

import json


VALID_REQUEST_TYPES = {
    "server_status",
    "add_task",
    "list_tasks",
    "complete_task",
    "delete_task"
}


def create_response(success, message, data=None):
    """
    Create a standard response dictionary.
    """
    return {
        "success": success,
        "message": message,
        "data": data
    }


def encode_message(message):
    """
    Convert a Python dictionary into a JSON string.
    """
    try:
        return json.dumps(message)
    except TypeError:
        return json.dumps(
            create_response(False, "Message could not be encoded as JSON.")
        )


def decode_message(message_text):
    """
    Convert a JSON string into a Python dictionary.
    """
    try:
        decoded_message = json.loads(message_text)

        if not isinstance(decoded_message, dict):
            return create_response(False, "Decoded message must be a JSON object.")

        return decoded_message

    except json.JSONDecodeError:
        return create_response(False, "Invalid JSON message.")


def validate_request(request):
    """
    Validate that a request has the required structure.
    """
    if not isinstance(request, dict):
        return create_response(False, "Request must be a dictionary.")

    request_type = request.get("request_type")

    if not request_type:
        return create_response(False, "Request is missing request_type.")

    if request_type not in VALID_REQUEST_TYPES:
        return create_response(False, f"Unknown request_type: {request_type}")

    if request_type == "add_task":
        task = request.get("task")

        if not isinstance(task, dict):
            return create_response(False, "add_task request must include a task object.")

        title = task.get("title", "")

        if not title or not title.strip():
            return create_response(False, "Task title cannot be empty.")

    if request_type in {"complete_task", "delete_task"}:
        task_id = request.get("task_id")

        if not isinstance(task_id, int):
            return create_response(False, f"{request_type} request must include an integer task_id.")

    return create_response(True, "Request is valid.")