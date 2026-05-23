"""
Unit tests for the task manager logic.
These tests do not require the networking server to run.
"""

import os
import unittest

from task_manager import (
    add_task,
    complete_task,
    delete_task,
    get_next_task_id,
    list_tasks,
    load_tasks,
    save_tasks
)


class TestTaskManager(unittest.TestCase):

    def setUp(self):
        """
        Create a temporary test file path before each test.
        """
        self.test_file = "test_tasks.json"

        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def tearDown(self):
        """
        Remove the temporary test file after each test.
        """
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_get_next_task_id_empty_list_returns_one(self):
        tasks = []

        next_id = get_next_task_id(tasks)

        self.assertEqual(next_id, 1)

    def test_get_next_task_id_returns_highest_id_plus_one(self):
        tasks = [
            {"id": 1, "title": "Task one"},
            {"id": 4, "title": "Task four"},
            {"id": 2, "title": "Task two"}
        ]

        next_id = get_next_task_id(tasks)

        self.assertEqual(next_id, 5)

    def test_add_task_adds_task_to_list(self):
        tasks = []

        result = add_task(tasks, "Finish networking module", "Build TCP project")

        self.assertTrue(result["success"])
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0]["title"], "Finish networking module")
        self.assertEqual(tasks[0]["description"], "Build TCP project")
        self.assertFalse(tasks[0]["completed"])

    def test_add_task_rejects_empty_title(self):
        tasks = []

        result = add_task(tasks, "   ")

        self.assertFalse(result["success"])
        self.assertEqual(len(tasks), 0)
        self.assertIsNone(result["task"])

    def test_list_tasks_returns_all_tasks(self):
        tasks = [
            {
                "id": 1,
                "title": "Test task",
                "description": "",
                "completed": False
            }
        ]

        result = list_tasks(tasks)

        self.assertTrue(result["success"])
        self.assertEqual(len(result["tasks"]), 1)
        self.assertEqual(result["tasks"][0]["title"], "Test task")

    def test_complete_task_marks_task_complete(self):
        tasks = [
            {
                "id": 1,
                "title": "Test task",
                "description": "",
                "completed": False
            }
        ]

        result = complete_task(tasks, 1)

        self.assertTrue(result["success"])
        self.assertTrue(tasks[0]["completed"])

    def test_complete_task_returns_error_for_missing_id(self):
        tasks = [
            {
                "id": 1,
                "title": "Test task",
                "description": "",
                "completed": False
            }
        ]

        result = complete_task(tasks, 99)

        self.assertFalse(result["success"])
        self.assertIsNone(result["task"])

    def test_delete_task_removes_task(self):
        tasks = [
            {
                "id": 1,
                "title": "Test task",
                "description": "",
                "completed": False
            }
        ]

        result = delete_task(tasks, 1)

        self.assertTrue(result["success"])
        self.assertEqual(len(tasks), 0)

    def test_delete_task_returns_error_for_missing_id(self):
        tasks = [
            {
                "id": 1,
                "title": "Test task",
                "description": "",
                "completed": False
            }
        ]

        result = delete_task(tasks, 99)

        self.assertFalse(result["success"])
        self.assertEqual(len(tasks), 1)

    def test_save_and_load_tasks(self):
        tasks = [
            {
                "id": 1,
                "title": "Saved task",
                "description": "Testing save and load",
                "completed": False
            }
        ]

        save_result = save_tasks(tasks, self.test_file)
        loaded_tasks = load_tasks(self.test_file)

        self.assertTrue(save_result["success"])
        self.assertEqual(len(loaded_tasks), 1)
        self.assertEqual(loaded_tasks[0]["title"], "Saved task")


if __name__ == "__main__":
    unittest.main()