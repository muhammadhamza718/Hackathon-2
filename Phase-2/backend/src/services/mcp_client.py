import asyncio
from typing import List, Dict, Any, Optional
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from agents import function_tool
import logging
import os
import sys

logger = logging.getLogger(__name__)

class TodoMCPClient:
    def __init__(self, server_path: str):
        self.server_path = server_path
        self._session: Optional[ClientSession] = None
        self._exit_stack = None

    async def connect(self):
        """Connect to the MCP server via stdio"""
        # Determine the server command (using python from the environment)
        server_params = StdioServerParameters(
            command=sys.executable,
            args=[self.server_path],
            env={**os.environ, "PYTHONPATH": os.path.dirname(os.path.dirname(self.server_path))}
        )
        
        from contextlib import AsyncExitStack
        self._exit_stack = AsyncExitStack()
        
        logger.info(f"Connecting to MCP Server at: {self.server_path}")
        read, write = await self._exit_stack.enter_async_context(stdio_client(server_params))
        self._session = await self._exit_stack.enter_async_context(ClientSession(read, write))
        
        await self._session.initialize()
        logger.info("✅ Connected to MCP Server")

    async def get_agent_tools(self, user_id: str):
        """
        Discover tools from the MCP server and wrap them for the OpenAI Agent.
        This dynamically converts MCP tools into @function_tool decorated functions.
        """
        if not self._session:
            await self.connect()

        mcp_tools = await self._session.list_tools()
        
        agent_tools = []
        for tool in mcp_tools.tools:
            # We create a closure that calls the MCP tool
            tool_name = tool.name
            
            def create_tool_func(name):
                # Using a wrapper to capture 'name' and 'user_id'
                async def mcp_tool_wrapper(**kwargs) -> dict:
                    # Automatically inject user_id if required by the MCP tool
                    # Our refactored MCP tools all require user_id
                    kwargs["user_id"] = user_id
                    
                    logger.info(f"🔧 MCP Call: {name}({kwargs})")
                    result = await self._session.call_tool(name, kwargs)
                    
                    # Convert MCP result to a dict that the agent understands
                    # result.content is usually a list of TextContent/ImageContent
                    if result.isError:
                        return {"success": False, "message": str(result.content)}
                    
                    # Try to parse the first text content as JSON if possible, else return as string
                    # Our specific MCP responses are JSON-serializable models
                    text = result.content[0].text if result.content else "{}"
                    try:
                        import json
                        return json.loads(text)
                    except:
                        return {"result": text}
                
                # We need to manually set the docstring and name for the agent to use
                mcp_tool_wrapper.__doc__ = tool.description
                mcp_tool_wrapper.__name__ = name
                return function_tool(mcp_tool_wrapper)

            agent_tools.append(create_tool_func(tool_name))
        
        return agent_tools

    async def close(self):
        if self._exit_stack:
            await self._exit_stack.aclose()
            logger.info("Closed MCP Client connection")
