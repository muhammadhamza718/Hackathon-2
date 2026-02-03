"""
Unit tests for TaskManager CRUD operations
"""
import unittest
import tempfile
import os
from src.todo_app import TaskManager, Priority, Category


class TestTaskManagerCRUD(unittest.TestCase):

    def setUp(self):
        # Create a temporary file for testing
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.json')
        self.temp_file.close()
        self.tm = TaskManager(data_file=self.temp_file.name)

    def tearDown(self):
        # Remove the temporary file
        if os.path.exists(self.temp_file.name):
            os.remove(self.temp_file.name)

    def test_add_task_success(self):
        task = self.tm.add_task("Test task", "Test description", Category.WORK.value, Priority.HIGH.value)

        self.assertEqual(task.title, "Test task")
        self.assertEqual(task.description, "Test description")
        self.assertEqual(task.category, Category.WORK.value)
        self.assertEqual(task.priority, Priority.HIGH.value)
        self.assertEqual(task.completed, False)
        self.assertIsNotNone(task.id)
        self.assertIn(task, self.tm.get_all_tasks())

    def test_add_task_validation_errors(self):
        # Test title validation
        with self.assertRaises(ValueError):
            self.tm.add_task("")  # Empty title

        with self.assertRaises(ValueError):
            self.tm.add_task("A" * 51)  # Title too long

        # Test description validation
        with self.assertRaises(ValueError):
            self.tm.add_task("Valid title", "A" * 201)  # Description too long

        # Test category validation
        with self.assertRaises(ValueError):
            self.tm.add_task("Valid title", "Valid description", "INVALID_CATEGORY")

        # Test priority validation
        with self.assertRaises(ValueError):
            self.tm.add_task("Valid title", "Valid description", Category.WORK.value, "INVALID_PRIORITY")

    def test_get_task(self):
        task = self.tm.add_task("Test task")

        retrieved_task = self.tm.get_task(task.id)
        self.assertIsNotNone(retrieved_task)
        self.assertEqual(retrieved_task.id, task.id)
        self.assertEqual(retrieved_task.title, task.title)

        # Test getting non-existent task
        non_existent = self.tm.get_task(999)
        self.assertIsNone(non_existent)

    def test_update_task(self):
        task = self.tm.add_task("Original title", "Original description", Category.GENERAL.value, Priority.MEDIUM.value)

        updated_task = self.tm.update_task(
            task.id,
            title="Updated title",
            description="Updated description",
            category=Category.WORK.value,
            priority=Priority.HIGH.value,
            completed=True
        )

        self.assertIsNotNone(updated_task)
        self.assertEqual(updated_task.title, "Updated title")
        self.assertEqual(updated_task.description, "Updated description")
        self.assertEqual(updated_task.category, Category.WORK.value)
        self.assertEqual(updated_task.priority, Priority.HIGH.value)
        self.assertEqual(updated_task.completed, True)

    def test_update_task_partial_fields(self):
        task = self.tm.add_task("Original title", "Original description", Category.GENERAL.value)

        # Update only title
        updated_task = self.tm.update_task(task.id, title="New title")

        self.assertEqual(updated_task.title, "New title")
        self.assertEqual(updated_task.description, "Original description")  # Should remain unchanged
        self.assertEqual(updated_task.category, Category.GENERAL.value)  # Should remain unchanged

    def test_update_nonexistent_task(self):
        result = self.tm.update_task(999, title="New title")
        self.assertIsNone(result)

    def test_update_task_validation_errors(self):
        task = self.tm.add_task("Test task")

        # Test title validation on update
        with self.assertRaises(ValueError):
            self.tm.update_task(task.id, title="A" * 51)  # Title too long

        # Test description validation on update
        with self.assertRaises(ValueError):
            self.tm.update_task(task.id, description="A" * 201)  # Description too long

        # Test category validation on update
        with self.assertRaises(ValueError):
            self.tm.update_task(task.id, category="INVALID_CATEGORY")

        # Test priority validation on update
        with self.assertRaises(ValueError):
            self.tm.update_task(task.id, priority="INVALID_PRIORITY")

    def test_delete_task(self):
        task = self.tm.add_task("Test task")

        # Verify task exists
        self.assertIsNotNone(self.tm.get_task(task.id))

        # Delete task
        result = self.tm.delete_task(task.id)

        # Verify deletion
        self.assertTrue(result)
        self.assertIsNone(self.tm.get_task(task.id))

    def test_delete_nonexistent_task(self):
        result = self.tm.delete_task(999)
        self.assertFalse(result)

    def test_toggle_completion(self):
        task = self.tm.add_task("Test task")

        # Initially should be False
        self.assertFalse(task.completed)

        # Toggle to True
        toggled_task = self.tm.toggle_completion(task.id)
        self.assertTrue(toggled_task.completed)

        # Toggle back to False
        toggled_task = self.tm.toggle_completion(task.id)
        self.assertFalse(toggled_task.completed)

    def test_toggle_nonexistent_task(self):
        result = self.tm.toggle_completion(999)
        self.assertIsNone(result)

    def test_get_all_tasks(self):
        # Add multiple tasks
        task1 = self.tm.add_task("Task 1")
        task2 = self.tm.add_task("Task 2", category=Category.WORK.value)
        task3 = self.tm.add_task("Task 3", category=Category.PERSONAL.value)

        all_tasks = self.tm.get_all_tasks()

        self.assertEqual(len(all_tasks), 3)
        self.assertIn(task1, all_tasks)
        self.assertIn(task2, all_tasks)
        self.assertIn(task3, all_tasks)

    def test_get_tasks_by_category(self):
        # Add tasks in different categories
        work_task1 = self.tm.add_task("Work task 1", category=Category.WORK.value)
        work_task2 = self.tm.add_task("Work task 2", category=Category.WORK.value)
        personal_task = self.tm.add_task("Personal task", category=Category.PERSONAL.value)

        work_tasks = self.tm.get_tasks_by_category(Category.WORK.value)
        personal_tasks = self.tm.get_tasks_by_category(Category.PERSONAL.value)

        self.assertEqual(len(work_tasks), 2)
        self.assertIn(work_task1, work_tasks)
        self.assertIn(work_task2, work_tasks)
        self.assertNotIn(personal_task, work_tasks)

        self.assertEqual(len(personal_tasks), 1)
        self.assertIn(personal_task, personal_tasks)

    def test_get_tasks_by_category_validation(self):
        with self.assertRaises(ValueError):
            self.tm.get_tasks_by_category("INVALID_CATEGORY")

    def test_search_tasks(self):
        # Add tasks with different content
        task1 = self.tm.add_task("Buy groceries", "Milk and eggs")
        task2 = self.tm.add_task("Finish report", "Complete the quarterly report")
        task3 = self.tm.add_task("Call mom", "Schedule doctor appointment")

        # Search in titles
        results = self.tm.search_tasks("report")
        self.assertEqual(len(results), 1)
        self.assertIn(task2, results)

        # Search in descriptions
        results = self.tm.search_tasks("milk")
        self.assertEqual(len(results), 1)
        self.assertIn(task1, results)

        # Case insensitive search
        results = self.tm.search_tasks("MILK")
        self.assertEqual(len(results), 1)
        self.assertIn(task1, results)

        # Search for non-existent term
        results = self.tm.search_tasks("nonexistent")
        self.assertEqual(len(results), 0)

        # Empty search should return all
        results = self.tm.search_tasks("")
        self.assertEqual(len(results), 3)

    def test_filter_tasks(self):
        # Add tasks with different properties
        task1 = self.tm.add_task("Task 1", priority=Priority.LOW.value, category=Category.WORK.value)
        task2 = self.tm.add_task("Task 2", priority=Priority.HIGH.value, category=Category.WORK.value)
        # Update task2 to be completed
        self.tm.update_task(task2.id, completed=True)

        task3 = self.tm.add_task("Task 3", priority=Priority.MEDIUM.value, category=Category.PERSONAL.value)

        # Filter by completion
        completed_tasks = self.tm.filter_tasks(completed=True)
        pending_tasks = self.tm.filter_tasks(completed=False)

        self.assertEqual(len(completed_tasks), 1)
        self.assertIn(task2, completed_tasks)

        self.assertEqual(len(pending_tasks), 2)
        self.assertIn(task1, pending_tasks)
        self.assertIn(task3, pending_tasks)

        # Filter by priority
        high_priority_tasks = self.tm.filter_tasks(priority=Priority.HIGH.value)
        self.assertEqual(len(high_priority_tasks), 1)
        self.assertIn(task2, high_priority_tasks)

        # Filter by category
        work_tasks = self.tm.filter_tasks(category=Category.WORK.value)
        self.assertEqual(len(work_tasks), 2)
        self.assertIn(task1, work_tasks)
        self.assertIn(task2, work_tasks)

        # Combined filters
        completed_work_tasks = self.tm.filter_tasks(completed=True, category=Category.WORK.value)
        self.assertEqual(len(completed_work_tasks), 1)
        self.assertIn(task2, completed_work_tasks)

    def test_filter_tasks_validation(self):
        with self.assertRaises(ValueError):
            self.tm.filter_tasks(priority="INVALID_PRIORITY")

        with self.assertRaises(ValueError):
            self.tm.filter_tasks(category="INVALID_CATEGORY")


if __name__ == '__main__':
    unittest.main()