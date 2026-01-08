from __future__ import annotations
from typing import Any, Dict, List, Optional, AsyncIterator
import logging
from datetime import datetime
import os

from chatkit.server import ChatKitServer
from chatkit.agents import AgentContext, simple_to_agent_input, stream_agent_response
from src.services.chat_store import SqlModelStore
from chatkit.types import ThreadMetadata, ThreadStreamEvent, UserMessageItem
from chatkit.store import Store
from agents import Runner

# Import agent creation and MCP client
from agent import create_todo_agent
from src.services.mcp_client import TodoMCPClient

logger = logging.getLogger(__name__)

class TodoChatServer(ChatKitServer):
    """
    Standard ChatKit server for Phase 2.
    Simplified to use Gemini directly WITHOUT MCP (which is Phase 3).
    """

    def __init__(self, store: Optional[Store] = None) -> None:
        # Use database-backed store for Phase-3 compliance
        if store is None:
            self.store = SqlModelStore()
        else:
            self.store = store
            
        super().__init__(self.store)
        logger.info(f"✅ TodoChatServer initialized (Phase 2 - No MCP)")

    async def respond(
        self,
        thread: ThreadMetadata,
        item: UserMessageItem | None,
        context: dict[str, Any],
    ) -> AsyncIterator[ThreadStreamEvent]:
        """Handle incoming messages"""
        
        user_id = context.get("user_id")
        if not user_id:
            logger.error("❌ No user_id in context! ChatKit should be authenticated.")
            # from chatkit.types import TextMessage
            # yield TextMessage(role="assistant", content="Authentication required")
            return

        logger.info(f"Turn Start: Thread={thread.id}, User={user_id}")

        try:
            # Phase 2 Simplification: LOCAL TOOLS
            # We define tools here that use the existing backend services directly
            from src.services.todo_service import TodoService
            from models.task import TaskCreate, TaskUpdate
            from sqlmodel import Session
            from src.models.database import sync_engine
            from agents import function_tool

            # 1. Define Tool Functions
            def add_task(title: str, description: str = "") -> dict:
                """Create a new task."""
                logger.info(f"🔧 CALLING LOCAL TOOL: add_task(title={title})")
                with Session(sync_engine) as session:
                    task = TodoService.create_todo_sync(session, TaskCreate(title=title, description=description), user_id)
                    logger.info(f"✅ LOCAL TOOL RESULT: {task.id}")
                    return {"id": task.id, "title": task.title, "status": "created"}

            def list_tasks(status: str = "all") -> list:
                 """List tasks. Status can be 'all', 'pending', or 'completed'."""
                 logger.info(f"🔧 CALLING LOCAL TOOL: list_tasks(status={status})")
                 completed_filter = None
                 if status == "pending": completed_filter = False
                 elif status == "completed": completed_filter = True
                 
                 with Session(sync_engine) as session:
                     tasks = TodoService.get_todos_sync(session, user_id, completed=completed_filter)
                     logger.info(f"✅ LOCAL TOOL RESULT: Found {len(tasks)} tasks")
                     return [{"id": t.id, "title": t.title, "completed": t.completed} for t in tasks]

            def update_task(task_id: int, title: str = None, descriptor: str = None) -> dict:
                """Update a task's title or description."""
                logger.info(f"🔧 CALLING LOCAL TOOL: update_task(id={task_id})")
                with Session(sync_engine) as session:
                     update_data = TaskUpdate(title=title, description=descriptor)
                     task = TodoService.update_todo_sync(session, task_id, user_id, update_data)
                     if task:
                         return {"id": task.id, "title": task.title, "status": "updated"}
                     return {"error": "Task not found"}

            def delete_task(task_id: int) -> dict:
                """Delete a task."""
                logger.info(f"🔧 CALLING LOCAL TOOL: delete_task(id={task_id})")
                with Session(sync_engine) as session:
                    success = TodoService.delete_todo_sync(session, task_id, user_id)
                    if success:
                        return {"id": task_id, "status": "deleted"}
                    return {"error": "Task not found"}

            def complete_task(task_id: int) -> dict:
                """Mark a task as complete."""
                logger.info(f"🔧 CALLING LOCAL TOOL: complete_task(id={task_id})")
                with Session(sync_engine) as session:
                    task = TodoService.complete_todo_sync(session, task_id, user_id)
                    if task:
                        return {"id": task.id, "status": "completed", "title": task.title}
                    return {"error": "Task not found"}

            # 2. Wrap them for the agent
            tools = [
                function_tool(add_task),
                function_tool(list_tasks),
                function_tool(update_task),
                function_tool(delete_task),
                function_tool(complete_task)
            ]
            
            # 3. Create agent with user-specific LOCAL tools
            items_page = await self.store.load_thread_items(
                thread.id,
                after=None,
                limit=50,
                order="desc",
                context=context
            )
            items = list(reversed(items_page.data))
            
            # 3. Create agent with NO tools (Pure Chat)
            agent = create_todo_agent(tools=tools)

            # 4. Prepare Agent Context
            agent_context = AgentContext(
                thread=thread,
                store=self.store,
                request_context=context,
            )

            # 5. Convert items to agent input
            agent_input = await simple_to_agent_input(items)

            # 6. Run Agent
            runner_result = Runner.run_streamed(
                agent,
                agent_input,
                context=agent_context
            )

            # 7. Stream back to ChatKit
            async for event in stream_agent_response(agent_context, runner_result):
                yield event

        except Exception as e:
            logger.exception(f"Error in TodoChatServer.respond: {str(e)}")
            # Fallback to text message for errors
            # from chatkit.types import TextMessage
            # yield TextMessage(role="assistant", content=f"Internal agent error: {str(e)}")
            pass
        finally:
            logger.info(f"Turn End: Thread={thread.id}")
