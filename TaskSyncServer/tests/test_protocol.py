"""
Unit tests for JSON message encoding, decoding, and request validation.
"""

import unittest

from protocol import (
    create_response,
    decode_message,
    encode_message,
    validate_request
)


class TestProtocol(unittest.TestCase):

    def test_create_response_returns_standard_response(self):
        response = create_response(True, "Test message.", {"value": 10})

        self.assertTrue(response["success"])
        self.assertEqual(response["message"], "Test message.")
        self.assertEqual(response["data"]["value"], 10)

    def test_encode_message_returns_json_string(self):
        message = {
            "request_type": "server_status"
        }

        encoded = encode_message(message)

        self.assertIsInstance(encoded, str)
        self.assertIn("server_status", encoded)

    def test_decode_message_returns_dictionary(self):
        message_text = '{"request_type": "server_status"}'

        decoded = decode_message(message_text)

        self.assertEqual(decoded["request_type"], "server_status")

    def test_decode_message_rejects_invalid_json(self):
        decoded = decode_message("{bad json")

        self.assertFalse(decoded["success"])
        self.assertEqual(decoded["message"], "Invalid JSON message.")

    def test_decode_message_rejects_json_array(self):
        decoded = decode_message('["server_status"]')

        self.assertFalse(decoded["success"])
        self.assertEqual(decoded["message"], "Decoded message must be a JSON object.")

    def test_validate_request_accepts_server_status(self):
        request = {
            "request_type": "server_status"
        }

        result = validate_request(request)

        self.assertTrue(result["success"])

    def test_validate_request_rejects_missing_request_type(self):
        request = {}

        result = validate_request(request)

        self.assertFalse(result["success"])
        self.assertEqual(result["message"], "Request is missing request_type.")

    def test_validate_request_rejects_unknown_request_type(self):
        request = {
            "request_type": "bad_request"
        }

        result = validate_request(request)

        self.assertFalse(result["success"])
        self.assertEqual(result["message"], "Unknown request_type: bad_request")

    def test_validate_request_accepts_valid_add_task(self):
        request = {
            "request_type": "add_task",
            "task": {
                "title": "Finish networking project",
                "description": "Build TCP client-server project"
            }
        }

        result = validate_request(request)

        self.assertTrue(result["success"])

    def test_validate_request_rejects_add_task_without_task_object(self):
        request = {
            "request_type": "add_task"
        }

        result = validate_request(request)

        self.assertFalse(result["success"])
        self.assertEqual(result["message"], "add_task request must include a task object.")

    def test_validate_request_rejects_add_task_with_empty_title(self):
        request = {
            "request_type": "add_task",
            "task": {
                "title": "   "
            }
        }

        result = validate_request(request)

        self.assertFalse(result["success"])
        self.assertEqual(result["message"], "Task title cannot be empty.")

    def test_validate_request_accepts_complete_task_with_integer_id(self):
        request = {
            "request_type": "complete_task",
            "task_id": 1
        }

        result = validate_request(request)

        self.assertTrue(result["success"])

    def test_validate_request_rejects_complete_task_without_integer_id(self):
        request = {
            "request_type": "complete_task",
            "task_id": "1"
        }

        result = validate_request(request)

        self.assertFalse(result["success"])

    def test_validate_request_accepts_delete_task_with_integer_id(self):
        request = {
            "request_type": "delete_task",
            "task_id": 1
        }

        result = validate_request(request)

        self.assertTrue(result["success"])

    def test_validate_request_rejects_delete_task_without_integer_id(self):
        request = {
            "request_type": "delete_task",
            "task_id": "1"
        }

        result = validate_request(request)

        self.assertFalse(result["success"])


if __name__ == "__main__":
    unittest.main()