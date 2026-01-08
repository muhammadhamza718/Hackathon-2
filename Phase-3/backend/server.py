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
    Standard ChatKit server with MCP integration for todos.
    Ensures that for every message turn, it connects to the MCP server,
    discovers tools for the specific user, and runs the agent with those tools.
    """

    def __init__(self, store: Optional[Store] = None) -> None:
        # Use database-backed store for Phase-3 compliance
        if store is None:
            self.store = SqlModelStore()
        else:
            self.store = store
            
        super().__init__(self.store)
        
        # Determine MCP server path
        mcp_server_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "mcp-server", "src", "todo_operations.py")
        self.mcp_client = TodoMCPClient(os.path.abspath(mcp_server_path))
        logger.info(f"✅ TodoChatServer initialized with MCP Client (Server path: {mcp_server_path})")

    async def respond(
        self,
        thread: ThreadMetadata,
        item: UserMessageItem | None,
        context: dict[str, Any],
    ) -> AsyncIterator[ThreadStreamEvent]:
        """Handle incoming messages following the stateless Phase-3 design"""
        
        user_id = context.get("user_id")
        if not user_id:
            logger.error("❌ No user_id in context! ChatKit should be authenticated.")
            yield {"error": "Authentication required"}
            return

        logger.info(f"Turn Start: Thread={thread.id}, User={user_id}")

        try:
            # 1. Connect to MCP and get tools for THIS user
            await self.mcp_client.connect()
            tools = await self.mcp_client.get_agent_tools(user_id)
            
            # 2. Load history (SqlModelStore handles user filtering via context)
            items_page = await self.store.load_thread_items(
                thread.id,
                after=None,
                limit=50,
                order="desc",
                context=context
            )
            items = list(reversed(items_page.data))
            
            # 3. Create agent with user-specific MCP tools
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
            yield {"error": f"Internal agent error: {str(e)}"}
        finally:
            # Clean up MCP connection after turn
            await self.mcp_client.close()
            logger.info(f"Turn End: Thread={thread.id}")
