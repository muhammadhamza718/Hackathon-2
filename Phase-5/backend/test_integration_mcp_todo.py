import pytest
import asyncio
from unittest.mock import Mock, patch, AsyncMock
import sys
import os
from pathlib import Path
from sqlmodel import create_engine, Session, SQLModel, select

# Add the mcp-server/src to the path so we can import modules
sys.path.insert(0, str(Path(__file__).parent.parent / "mcp-server" / "src"))

from todo_operations import MCPTaskService, Task

@pytest.fixture
def mock_service():
    """Create a service with a mock in-memory database"""
    # Use an in-memory SQLite database for testing
    engine = create_engine("sqlite:///:memory:")
    # Create tables
    SQLModel.metadata.create_all(bind=engine)

    # Patch the engine in the service
    with patch('todo_operations.create_engine', return_value=engine):
        service = MCPTaskService()
        yield service

def test_add_task_integration(mock_service):
    """Test standard task creation with user_id"""
    user_id = "test-user-123"
    title = "Buy groceries"
    description = "Milk and bread"

    result = mock_service.add_task(user_id, title, description)

    assert result["success"] is True
    assert result["task"]["title"] == title
    assert result["task"]["user_id"] == user_id
    assert result["task"]["completed"] is False

    # Verify persistence
    with Session(mock_service.engine) as session:
        task = session.exec(select(Task).where(Task.id == result["task"]["id"])).first()
        assert task is not None
        assert task.user_id == user_id

def test_list_tasks_isolation(mock_service):
    """Test that tasks are filtered correctly by user_id"""
    user1 = "user-1"
    user2 = "user-2"

    mock_service.add_task(user1, "User 1 Task", None)
    mock_service.add_task(user2, "User 2 Task", None)

    # Check User 1
    res1 = mock_service.list_tasks(user1)
    assert len(res1["tasks"]) == 1
    assert res1["tasks"][0]["title"] == "User 1 Task"

    # Check User 2
    res2 = mock_service.list_tasks(user2)
    assert len(res2["tasks"]) == 1
    assert res2["tasks"][0]["title"] == "User 2 Task"

def test_complete_task_integration(mock_service):
    """Test marking a task as completed"""
    user_id = "test-user"
    add_res = mock_service.add_task(user_id, "Complete me", None)
    task_id = add_res["task"]["id"]

    result = mock_service.complete_task(user_id, task_id)
    assert result["success"] is True

    # Verify in DB
    with Session(mock_service.engine) as session:
        task = session.get(Task, task_id)
        assert task.completed is True

def test_delete_task_integration(mock_service):
    """Test deleting a task"""
    user_id = "test-user"
    add_res = mock_service.add_task(user_id, "Delete me", None)
    task_id = add_res["task"]["id"]

    result = mock_service.delete_task(user_id, task_id)
    assert result["success"] is True

    # Verify gone
    with Session(mock_service.engine) as session:
        task = session.get(Task, task_id)
        assert task is None

def test_error_wrong_user(mock_service):
    """Test that one user cannot modify another user's task"""
    user1 = "user-1"
    user2 = "user-2"
    
    add_res = mock_service.add_task(user1, "Secret Task", None)
    task_id = add_res["task"]["id"]

    # User 2 tries to complete User 1's task
    result = mock_service.complete_task(user2, task_id)
    assert result["success"] is False
    assert "not found" in result["message"].lower()

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
