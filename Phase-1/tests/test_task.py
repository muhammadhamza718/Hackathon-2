"""
Unit tests for Task validation methods
"""
import unittest
from datetime import datetime
from src.todo_app import Task, Priority, Category


class TestTask(unittest.TestCase):

    def test_validate_title(self):
        task = Task(1, "Valid title")

        # Test valid titles
        self.assertTrue(task.validate_title("A"))
        self.assertTrue(task.validate_title("A" * 50))

        # Test invalid titles
        self.assertFalse(task.validate_title(""))  # Too short
        self.assertFalse(task.validate_title("A" * 51))  # Too long

    def test_validate_description(self):
        task = Task(1, "Valid title")

        # Test valid descriptions
        self.assertTrue(task.validate_description(""))
        self.assertTrue(task.validate_description("A"))
        self.assertTrue(task.validate_description("A" * 200))

        # Test invalid descriptions
        self.assertFalse(task.validate_description("A" * 201))  # Too long

    def test_validate_category(self):
        task = Task(1, "Valid title")

        # Test valid categories
        self.assertTrue(task.validate_category(Category.GENERAL.value))
        self.assertTrue(task.validate_category(Category.WORK.value))
        self.assertTrue(task.validate_category(Category.PERSONAL.value))

        # Test invalid category
        self.assertFalse(task.validate_category("INVALID"))

    def test_validate_priority(self):
        task = Task(1, "Valid title")

        # Test valid priorities
        self.assertTrue(task.validate_priority(Priority.LOW.value))
        self.assertTrue(task.validate_priority(Priority.MEDIUM.value))
        self.assertTrue(task.validate_priority(Priority.HIGH.value))

        # Test invalid priority
        self.assertFalse(task.validate_priority("INVALID"))

    def test_task_creation_with_valid_data(self):
        created_at = datetime.now()
        task = Task(
            id=1,
            title="Test task",
            description="Test description",
            category=Category.WORK.value,
            completed=False,
            priority=Priority.HIGH.value,
            created_at=created_at
        )

        self.assertEqual(task.id, 1)
        self.assertEqual(task.title, "Test task")
        self.assertEqual(task.description, "Test description")
        self.assertEqual(task.category, Category.WORK.value)
        self.assertEqual(task.completed, False)
        self.assertEqual(task.priority, Priority.HIGH.value)
        self.assertEqual(task.created_at, created_at)

    def test_task_creation_with_invalid_category_defaults_to_general(self):
        task = Task(
            id=1,
            title="Test task",
            category="INVALID_CATEGORY"
        )

        self.assertEqual(task.category, Category.GENERAL.value)

    def test_task_creation_with_invalid_priority_defaults_to_medium(self):
        task = Task(
            id=1,
            title="Test task",
            priority="INVALID_PRIORITY"
        )

        self.assertEqual(task.priority, Priority.MEDIUM.value)

    def test_to_dict_and_from_dict_roundtrip(self):
        original_task = Task(
            id=1,
            title="Test task",
            description="Test description",
            category=Category.WORK.value,
            completed=True,
            priority=Priority.HIGH.value
        )

        # Convert to dict and back
        task_dict = original_task.to_dict()
        reconstructed_task = Task.from_dict(task_dict)

        # Check that all fields match
        self.assertEqual(original_task.id, reconstructed_task.id)
        self.assertEqual(original_task.title, reconstructed_task.title)
        self.assertEqual(original_task.description, reconstructed_task.description)
        self.assertEqual(original_task.category, reconstructed_task.category)
        self.assertEqual(original_task.completed, reconstructed_task.completed)
        self.assertEqual(original_task.priority, reconstructed_task.priority)


if __name__ == '__main__':
    unittest.main()