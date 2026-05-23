"""
Integration tests for Task Sync Server.

These tests start the real TCP server in a background thread, send real client
requests through localhost, and verify the server responses.
"""

import os
import threading
import time
import unittest

import server
from client import send_request


class TestNetworkIntegration(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """
        Start the server once in a background thread for all integration tests.
        """
        cls.test_task_file = "test_network_tasks.json"
        cls.test_host = "127.0.0.1"
        cls.test_port = 5051

        server.TASK_FILE = cls.test_task_file

        if os.path.exists(cls.test_task_file):
            os.remove(cls.test_task_file)

        cls.server_thread = threading.Thread(
            target=server.start_server,
            args=(cls.test_host, cls.test_port),
            daemon=True
        )

        cls.server_thread.start()
        time.sleep(0.25)

    def setUp(self):
        """
        Reset the test task file before each test.
        """
        with open(self.test_task_file, "w", encoding="utf-8") as file:
            file.write("[]")

    def tearDown(self):
        """
        Clear the test task file after each test.
        """
        with open(self.test_task_file, "w", encoding="utf-8") as file:
            file.write("[]")

    @classmethod
    def tearDownClass(cls):
        """
        Remove the temporary test file after integration tests finish.
        """
        if os.path.exists(cls.test_task_file):
            os.remove(cls.test_task_file)

    def test_server_status_over_tcp(self):
        request = {
            "request_type": "server_status"
        }

        response = send_request(request, self.test_host, self.test_port)

        self.assertTrue(response["success"])
        self.assertEqual(response["message"], "Server is running.")
        self.assertEqual(response["data"]["server"], "Task Sync Server")

    def test_add_task_over_tcp(self):
        request = {
            "request_type": "add_task",
            "task": {
                "title": "Integration test task",
                "description": "Sent over TCP"
            }
        }

        response = send_request(request, self.test_host, self.test_port)

        self.assertTrue(response["success"])
        self.assertEqual(response["message"], "Task added successfully.")
        self.assertEqual(response["data"]["title"], "Integration test task")

    def test_list_tasks_over_tcp(self):
        add_request = {
            "request_type": "add_task",
            "task": {
                "title": "Task to list",
                "description": "Testing list over TCP"
            }
        }

        send_request(add_request, self.test_host, self.test_port)

        list_request = {
            "request_type": "list_tasks"
        }

        response = send_request(list_request, self.test_host, self.test_port)

        self.assertTrue(response["success"])
        self.assertEqual(len(response["data"]), 1)
        self.assertEqual(response["data"][0]["title"], "Task to list")

    def test_complete_task_over_tcp(self):
        add_request = {
            "request_type": "add_task",
            "task": {
                "title": "Task to complete",
                "description": "Testing complete over TCP"
            }
        }

        add_response = send_request(add_request, self.test_host, self.test_port)
        task_id = add_response["data"]["id"]

        complete_request = {
            "request_type": "complete_task",
            "task_id": task_id
        }

        response = send_request(complete_request, self.test_host, self.test_port)

        self.assertTrue(response["success"])
        self.assertTrue(response["data"]["completed"])

    def test_delete_task_over_tcp(self):
        add_request = {
            "request_type": "add_task",
            "task": {
                "title": "Task to delete",
                "description": "Testing delete over TCP"
            }
        }

        add_response = send_request(add_request, self.test_host, self.test_port)
        task_id = add_response["data"]["id"]

        delete_request = {
            "request_type": "delete_task",
            "task_id": task_id
        }

        response = send_request(delete_request, self.test_host, self.test_port)

        self.assertTrue(response["success"])
        self.assertEqual(response["data"]["id"], task_id)

    def test_invalid_request_over_tcp(self):
        request = {
            "request_type": "not_real"
        }

        response = send_request(request, self.test_host, self.test_port)

        self.assertFalse(response["success"])
        self.assertEqual(response["message"], "Unknown request_type: not_real")


if __name__ == "__main__":
    unittest.main()