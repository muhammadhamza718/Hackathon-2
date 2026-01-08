"""
Unit tests for backend services and agent integration
Tests individual components and their integration with the agent system
"""

import pytest
import asyncio
from unittest.mock import Mock, MagicMock, patch, AsyncMock
import sys
from pathlib import Path

# Add the backend/src to the path so we can import modules
sys.path.insert(0, str(Path(__file__).parent / "src"))

from agents.agent import TodoAgent
from api.server import create_app
from models.todo import Todo
from models.database import get_session, engine
from services.todo_service import TodoService


def test_todo_agent_initialization():
    """Test that TodoAgent initializes correctly"""
    # Act
    agent = TodoAgent()

    # Assert
    assert agent is not None
    assert hasattr(agent, 'model')
    assert hasattr(agent, 'system_prompt')
    assert hasattr(agent, 'agent')
    assert hasattr(agent, 'thread')


@patch('agents.agent.openai_client')
def test_send_message_calls_openai_api(mock_openai_client):
    """Test that send_message properly calls the OpenAI API"""
    # Arrange
    agent = TodoAgent()

    # Mock the OpenAI client responses
    mock_thread = Mock()
    mock_thread.id = "test_thread_id"
    agent.thread = mock_thread

    mock_assistant = Mock()
    mock_assistant.id = "test_assistant_id"
    agent.agent = mock_assistant

    mock_run = Mock()
    mock_run.status = "completed"
    mock_openai_client.beta.threads.runs.create.return_value = mock_run
    mock_openai_client.beta.threads.runs.retrieve.return_value = mock_run

    mock_messages = Mock()
    mock_messages.data = []
    mock_openai_client.beta.threads.messages.list.return_value = mock_messages

    # Act
    response = agent.send_message("Test message")

    # Assert
    mock_openai_client.beta.threads.messages.create.assert_called_once()
    mock_openai_client.beta.threads.runs.create.assert_called_once()


def test_todo_model_creation():
    """Test Todo model creation and properties"""
    # Arrange
    content = "Test todo content"

    # Act
    todo = Todo(content=content, completed=False)

    # Assert
    assert todo.content == content
    assert todo.completed is False
    assert todo.id is None  # Should be None before saving to DB


def test_todo_service_crud_operations():
    """Test TodoService CRUD operations"""
    # Arrange
    service = TodoService()

    # Act - Create a todo
    created_todo = service.create_todo("Test todo", None)

    # Assert - Verify creation
    assert created_todo is not None
    assert created_todo.content == "Test todo"
    assert created_todo.completed is False

    # Act - Retrieve the todo
    retrieved_todo = service.get_todo(created_todo.id)

    # Assert - Verify retrieval
    assert retrieved_todo is not None
    assert retrieved_todo.id == created_todo.id
    assert retrieved_todo.content == "Test todo"

    # Act - Update the todo
    updated_todo = service.update_todo(created_todo.id, completed=True)

    # Assert - Verify update
    assert updated_todo is not None
    assert updated_todo.id == created_todo.id
    assert updated_todo.completed is True

    # Act - List todos
    todos = service.list_todos()

    # Assert - Verify listing
    assert len(todos) >= 1
    todo_ids = [t.id for t in todos]
    assert created_todo.id in todo_ids

    # Act - Delete the todo
    deleted = service.delete_todo(created_todo.id)

    # Assert - Verify deletion
    assert deleted is True

    # Verify it's gone
    deleted_todo = service.get_todo(created_todo.id)
    assert deleted_todo is None


@patch('api.server.openai_client')
def test_api_server_health_check(mock_openai_client):
    """Test the API server health check endpoint"""
    # Arrange
    app = create_app()
    client = app.test_client()

    # Act
    response = client.get('/health')

    # Assert
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'healthy'


@patch('api.server.openai_client')
def test_api_server_chat_endpoint(mock_openai_client):
    """Test the API server chat endpoint"""
    # Arrange
    app = create_app()
    client = app.test_client()

    # Mock the OpenAI client responses
    mock_thread = Mock()
    mock_thread.id = "test_thread_id"

    mock_assistant = Mock()
    mock_assistant.id = "test_assistant_id"

    mock_run = Mock()
    mock_run.status = "completed"

    # Configure the mocks
    mock_openai_client.beta.threads.create.return_value = mock_thread
    mock_openai_client.beta.threads.runs.create.return_value = mock_run
    mock_openai_client.beta.threads.runs.retrieve.return_value = mock_run

    mock_messages = Mock()
    mock_message = Mock()
    mock_message.role = "assistant"
    mock_text = Mock()
    mock_text.value = "Test response"
    mock_message.content = [Mock(text=mock_text)]
    mock_messages.data = [mock_message]
    mock_openai_client.beta.threads.messages.list.return_value = mock_messages

    # Act
    response = client.post('/chat', json={'message': 'Test message'})

    # Assert
    assert response.status_code == 200
    data = response.get_json()
    assert 'response' in data


def test_database_connection():
    """Test database connection and session management"""
    # Act & Assert - This mainly verifies the connection doesn't throw an exception
    try:
        # Try to get a session
        session_gen = get_session()
        session = next(session_gen)

        # Verify we can execute a simple query
        result = session.exec(Todo).all()

        # Close the session
        session.close()

        # Success means the connection worked
        assert True

    except Exception as e:
        # If there's an exception, the test should fail
        assert False, f"Database connection failed: {e}"


async def test_async_functions():
    """Test async functions work properly"""
    # Arrange
    agent = TodoAgent()

    # Act
    # Test that the MCP connection function is callable
    try:
        await agent.connect_to_mcp_server("http://localhost:8000")
        # If no exception, the function is properly defined
        assert True
    except Exception as e:
        # We expect this to fail due to no server running, but not due to function definition issues
        assert "Connection" in str(e) or "connect" in str(e).lower()


if __name__ == "__main__":
    # Run the tests
    pytest.main([__file__, "-v"])