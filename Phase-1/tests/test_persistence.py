"""
Unit tests for TaskManager data persistence functions
"""
import unittest
import tempfile
import os
import json
from datetime import datetime
from src.todo_app import TaskManager, Priority, Category


class TestTaskManagerPersistence(unittest.TestCase):

    def setUp(self):
        # Create temporary files for testing
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.json')
        self.temp_file.close()
        self.tm = TaskManager(data_file=self.temp_file.name)

    def tearDown(self):
        # Remove the temporary files
        if os.path.exists(self.temp_file.name):
            os.remove(self.temp_file.name)

        # Clean up potential backup file
        backup_file = self.temp_file.name + ".backup"
        if os.path.exists(backup_file):
            os.remove(backup_file)

    def test_save_to_file(self):
        # Add some tasks
        task1 = self.tm.add_task("Task 1", "Description 1", Category.WORK.value, Priority.HIGH.value)
        task2 = self.tm.add_task("Task 2", "Description 2", Category.PERSONAL.value, Priority.MEDIUM.value)
        self.tm.toggle_completion(task1.id)  # Mark one as completed

        # Save to file
        self.tm.save_to_file()

        # Verify file exists and has content
        self.assertTrue(os.path.exists(self.temp_file.name))

        with open(self.temp_file.name, 'r', encoding='utf-8') as f:
            data = json.load(f)

        self.assertEqual(data["version"], "1.0")
        self.assertIn("last_updated", data)
        self.assertEqual(len(data["tasks"]), 2)

        # Verify task data
        saved_task1 = next((t for t in data["tasks"] if t["id"] == task1.id), None)
        self.assertIsNotNone(saved_task1)
        self.assertEqual(saved_task1["title"], "Task 1")
        self.assertEqual(saved_task1["description"], "Description 1")
        self.assertEqual(saved_task1["category"], Category.WORK.value)
        self.assertEqual(saved_task1["priority"], Priority.HIGH.value)
        self.assertTrue(saved_task1["completed"])  # Should be True because we toggled it

    def test_load_from_file_existing(self):
        # Prepare test data
        test_data = {
            "version": "1.0",
            "last_updated": datetime.now().isoformat(),
            "tasks": [
                {
                    "id": 1,
                    "title": "Loaded task",
                    "description": "Loaded description",
                    "category": Category.WORK.value,
                    "completed": True,
                    "priority": Priority.HIGH.value,
                    "created_at": datetime.now().isoformat()
                },
                {
                    "id": 2,
                    "title": "Another loaded task",
                    "description": "Another description",
                    "category": Category.PERSONAL.value,
                    "completed": False,
                    "priority": Priority.LOW.value,
                    "created_at": datetime.now().isoformat()
                }
            ]
        }

        # Write test data to file
        with open(self.temp_file.name, 'w', encoding='utf-8') as f:
            json.dump(test_data, f, indent=2)

        # Create a new TaskManager to load from file
        new_tm = TaskManager(data_file=self.temp_file.name)

        # Verify tasks were loaded
        tasks = new_tm.get_all_tasks()
        self.assertEqual(len(tasks), 2)

        # Find and verify the first task
        loaded_task1 = new_tm.get_task(1)
        self.assertIsNotNone(loaded_task1)
        self.assertEqual(loaded_task1.title, "Loaded task")
        self.assertEqual(loaded_task1.description, "Loaded description")
        self.assertEqual(loaded_task1.category, Category.WORK.value)
        self.assertTrue(loaded_task1.completed)
        self.assertEqual(loaded_task1.priority, Priority.HIGH.value)

        # Find and verify the second task
        loaded_task2 = new_tm.get_task(2)
        self.assertIsNotNone(loaded_task2)
        self.assertEqual(loaded_task2.title, "Another loaded task")
        self.assertEqual(loaded_task2.description, "Another description")
        self.assertEqual(loaded_task2.category, Category.PERSONAL.value)
        self.assertFalse(loaded_task2.completed)
        self.assertEqual(loaded_task2.priority, Priority.LOW.value)

    def test_load_from_file_nonexistent(self):
        # Create TaskManager with non-existent file
        nonexistent_file = "nonexistent_file.json"
        if os.path.exists(nonexistent_file):
            os.remove(nonexistent_file)

        new_tm = TaskManager(data_file=nonexistent_file)

        # Should initialize with empty task list
        self.assertEqual(len(new_tm.get_all_tasks()), 0)
        self.assertEqual(new_tm.next_id, 1)

    def test_load_from_file_invalid_json(self):
        # Write invalid JSON to file
        with open(self.temp_file.name, 'w', encoding='utf-8') as f:
            f.write("invalid json content")

        # Create a new TaskManager to load from file
        new_tm = TaskManager(data_file=self.temp_file.name)

        # Should initialize with empty task list due to error
        self.assertEqual(len(new_tm.get_all_tasks()), 0)
        self.assertEqual(new_tm.next_id, 1)

    def test_backup_data(self):
        # Add a task and save
        task = self.tm.add_task("Backup test", "Test backup functionality")
        self.tm.save_to_file()

        # Create backup
        self.tm.backup_data()

        backup_file = self.temp_file.name + ".backup"
        self.assertTrue(os.path.exists(backup_file))

        # Verify backup content matches original
        with open(self.temp_file.name, 'r', encoding='utf-8') as original_f:
            original_content = original_f.read()

        with open(backup_file, 'r', encoding='utf-8') as backup_f:
            backup_content = backup_f.read()

        self.assertEqual(original_content, backup_content)

    def test_backup_data_no_original(self):
        # Try to backup when original file doesn't exist
        nonexistent_file = "nonexistent_for_backup.json"
        if os.path.exists(nonexistent_file):
            os.remove(nonexistent_file)

        tm_new = TaskManager(data_file=nonexistent_file)

        # Backup should do nothing when original file doesn't exist
        # (no exception should be raised)
        tm_new.backup_data()

        # Verify no backup file was created
        backup_file = nonexistent_file + ".backup"
        self.assertFalse(os.path.exists(backup_file))

    def test_persistence_roundtrip(self):
        # Add tasks to original manager
        original_task1 = self.tm.add_task("Roundtrip 1", "First roundtrip task", Category.WORK.value, Priority.HIGH.value)
        original_task2 = self.tm.add_task("Roundtrip 2", "Second roundtrip task", Category.PERSONAL.value, Priority.LOW.value)
        self.tm.toggle_completion(original_task1.id)  # Mark first as completed

        # Save to file
        self.tm.save_to_file()

        # Create new manager and load from file
        new_tm = TaskManager(data_file=self.temp_file.name)

        # Verify all data was preserved
        loaded_tasks = new_tm.get_all_tasks()
        self.assertEqual(len(loaded_tasks), 2)

        loaded_task1 = new_tm.get_task(original_task1.id)
        self.assertIsNotNone(loaded_task1)
        self.assertEqual(loaded_task1.title, original_task1.title)
        self.assertEqual(loaded_task1.description, original_task1.description)
        self.assertEqual(loaded_task1.category, original_task1.category)
        self.assertEqual(loaded_task1.priority, original_task1.priority)
        self.assertEqual(loaded_task1.completed, True)  # Should be True as we toggled it

        loaded_task2 = new_tm.get_task(original_task2.id)
        self.assertIsNotNone(loaded_task2)
        self.assertEqual(loaded_task2.title, original_task2.title)
        self.assertEqual(loaded_task2.description, original_task2.description)
        self.assertEqual(loaded_task2.category, original_task2.category)
        self.assertEqual(loaded_task2.priority, original_task2.priority)
        self.assertEqual(loaded_task2.completed, False)

        # Verify next_id was restored correctly
        new_task = new_tm.add_task("Next ID test", "Task to test next ID")
        self.assertEqual(new_task.id, max(original_task1.id, original_task2.id) + 1)


if __name__ == '__main__':
    unittest.main()