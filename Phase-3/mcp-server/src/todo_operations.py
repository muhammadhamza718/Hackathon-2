"""MCP server implementation for task operations aligned with Phase 3 spec"""

import asyncio
from typing import Dict, Any, List, Optional
from mcp.server import Server
from mcp.types import TextContent, Tool
import json
from datetime import datetime
import os
import uuid
from sqlmodel import create_engine, Session, select, SQLModel, Field
from pydantic import BaseModel, Field as PydanticField

# Setup logging
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("mcp-todo-server")

# Define the Task model representing the 'task' table
class Task(SQLModel, table=True):
    __tablename__ = "task"
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    user_id: str = Field(index=True)
    title: str = Field(index=True, max_length=500)
    description: Optional[str] = Field(default=None)
    completed: bool = Field(default=False, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)
    updated_at: datetime = Field(default_factory=datetime.utcnow, index=True)

# Spec-compliant Request/Response Models
class AddTaskRequest(BaseModel):
    user_id: str
    title: str = PydanticField(..., min_length=1, max_length=500)
    description: Optional[str] = None

class ListTasksRequest(BaseModel):
    user_id: str
    completed: Optional[bool] = None

class TaskIdRequest(BaseModel):
    user_id: str
    task_id: str

class UpdateTaskRequest(BaseModel):
    user_id: str
    task_id: str
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

class MCPTaskService:
    def __init__(self):
        database_url = os.getenv("DATABASE_URL")
        # Default to local sqlite if not provided, but spec implies Postgres for Phase 3
        if not database_url:
            logger.warning("DATABASE_URL not found, defaulting to local SQLite")
            database_url = "sqlite:///./todos.db"
        self.engine = create_engine(database_url)

    def add_task(self, user_id: str, title: str, description: Optional[str] = None) -> dict:
        try:
            with Session(self.engine) as session:
                new_task = Task(
                    user_id=user_id,
                    title=title.strip(),
                    description=description,
                    completed=False
                )
                session.add(new_task)
                session.commit()
                session.refresh(new_task)
                return {"success": True, "task": new_task.dict(), "message": f"Task '{title}' added."}
        except Exception as e:
            logger.error(f"Error adding task: {e}")
            return {"success": False, "message": str(e)}

    def list_tasks(self, user_id: str, completed: Optional[bool] = None) -> dict:
        try:
            with Session(self.engine) as session:
                statement = select(Task).where(Task.user_id == user_id)
                if completed is not None:
                    statement = statement.where(Task.completed == completed)
                
                results = session.exec(statement).all()
                return {"success": True, "tasks": [t.dict() for t in results]}
        except Exception as e:
            logger.error(f"Error listing tasks: {e}")
            return {"success": False, "message": str(e)}

    def complete_task(self, user_id: str, task_id: str) -> dict:
        try:
            with Session(self.engine) as session:
                task = session.exec(select(Task).where(Task.id == task_id, Task.user_id == user_id)).first()
                if not task: return {"success": False, "message": "Task not found"}
                
                task.completed = True
                task.updated_at = datetime.utcnow()
                session.add(task)
                session.commit()
                session.refresh(task)
                return {"success": True, "task": task.dict()}
        except Exception as e:
            logger.error(f"Error completing task: {e}")
            return {"success": False, "message": str(e)}

    def delete_task(self, user_id: str, task_id: str) -> dict:
        try:
            with Session(self.engine) as session:
                task = session.exec(select(Task).where(Task.id == task_id, Task.user_id == user_id)).first()
                if not task: return {"success": False, "message": "Task not found"}
                
                session.delete(task)
                session.commit()
                return {"success": True, "message": "Task deleted."}
        except Exception as e:
            logger.error(f"Error deleting task: {e}")
            return {"success": False, "message": str(e)}

    def update_task(self, user_id: str, task_id: str, title: Optional[str] = None, description: Optional[str] = None, completed: Optional[bool] = None) -> dict:
        try:
            with Session(self.engine) as session:
                task = session.exec(select(Task).where(Task.id == task_id, Task.user_id == user_id)).first()
                if not task: return {"success": False, "message": "Task not found"}
                
                if title is not None: task.title = title.strip()
                if description is not None: task.description = description
                if completed is not None: task.completed = completed
                
                task.updated_at = datetime.utcnow()
                session.add(task)
                session.commit()
                session.refresh(task)
                return {"success": True, "task": task.dict()}
        except Exception as e:
            logger.error(f"Error updating task: {e}")
            return {"success": False, "message": str(e)}

service = MCPTaskService()

async def create_mcp_server():
    server = Server("todo-mcp-server")

    @server.tool("add_task", "Add a new task")
    async def add_task(params: AddTaskRequest) -> dict:
        return service.add_task(params.user_id, params.title, params.description)

    @server.tool("list_tasks", "List tasks")
    async def list_tasks(params: ListTasksRequest) -> dict:
        return service.list_tasks(params.user_id, params.completed)

    @server.tool("complete_task", "Mark task as completed")
    async def complete_task(params: TaskIdRequest) -> dict:
        return service.complete_task(params.user_id, params.task_id)

    @server.tool("delete_task", "Delete task")
    async def delete_task(params: TaskIdRequest) -> dict:
        return service.delete_task(params.user_id, params.task_id)

    @server.tool("update_task", "Update task")
    async def update_task(params: UpdateTaskRequest) -> dict:
        return service.update_task(params.user_id, params.task_id, params.title, params.description, params.completed)

    return server

if __name__ == "__main__":
    async def main():
        from mcp.server.stdio import stdio_server
        server = await create_mcp_server()
        async with stdio_server() as (read, write):
            await server.run(read, write, server.create_initialization_options())
    
    asyncio.run(main())