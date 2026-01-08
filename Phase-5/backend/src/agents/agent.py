"""OpenAI Agent with MCP integration for todo operations"""

import os
from typing import Dict, Any, List, Optional
from openai import OpenAI
from openai.types.beta.threads.runs.run_step import RunStep
from openai.types.beta.threads.text import Text
from openai.types.beta.threads.message import Message
import asyncio
import json
from dotenv import load_dotenv
import httpx
import logging
from datetime import datetime

# Load environment variables
load_dotenv()

# Initialize OpenAI client
# Initialize OpenAI client
api_key = os.getenv("OPENAI_API_KEY")
base_url = None

if not api_key:
    # Try Gemini API Key
    gemini_key = os.getenv("GEMINI_API_KEY")
    if gemini_key:
        api_key = gemini_key
        base_url = "https://generativelanguage.googleapis.com/v1beta/openai/"

openai_client = OpenAI(
    api_key=api_key,
    base_url=base_url
)

# Setup centralized logging
from ..config.logging_config import get_logger, log_mcp_call, log_error
logger = get_logger(__name__)


class TodoAgent:
    def __init__(self):
        """Initialize the Todo Agent with MCP integration"""
        self.model = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")  # Updated to newer model if available
        self.system_prompt = """
        You are a helpful todo assistant. You can help users add, list, complete, delete, and update their todos.
        Use the appropriate MCP tools for these operations.
        Always respond in a friendly and helpful manner.
        """
        
        # Initialize conversation history
        self.messages = [
            {"role": "system", "content": self.system_prompt}
        ]

    def _get_tools(self) -> List[Dict[str, Any]]:
        """Define the tools available to the agent"""
        return [
            {
                "type": "function",
                "function": {
                    "name": "add_todo",
                    "description": "Add a new todo item",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "content": {
                                "type": "string",
                                "description": "The content of the todo item"
                            },
                            "due_date": {
                                "type": "string",
                                "description": "Optional due date in ISO format"
                            }
                        },
                        "required": ["content"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "list_todos",
                    "description": "List todos for the user with optional filtering and pagination",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "completed": {
                                "type": "boolean",
                                "description": "Filter by completion status (true for completed, false for pending, null for all)"
                            },
                            "limit": {
                                "type": "integer",
                                "description": "Maximum number of todos to return (pagination)",
                                "default": 50
                            },
                            "offset": {
                                "type": "integer",
                                "description": "Number of todos to skip (pagination)",
                                "default": 0
                            }
                        }
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "complete_todo",
                    "description": "Mark a todo as completed",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "todo_id": {
                                "type": "integer",
                                "description": "The ID of the todo to complete"
                            }
                        },
                        "required": ["todo_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "delete_todo",
                    "description": "Delete a todo",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "todo_id": {
                                "type": "integer",
                                "description": "The ID of the todo to delete"
                            }
                        },
                        "required": ["todo_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "update_todo",
                    "description": "Update a todo",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "todo_id": {
                                "type": "integer",
                                "description": "The ID of the todo to update"
                            },
                            "content": {
                                "type": "string",
                                "description": "The new content of the todo"
                            },
                            "completed": {
                                "type": "boolean",
                                "description": "The new completion status of the todo"
                            },
                            "due_date": {
                                "type": "string",
                                "description": "The new due date in ISO format"
                            }
                        },
                        "required": ["todo_id"]
                    }
                }
            }
        ]

    async def connect_to_mcp_server(self, mcp_url: Optional[str] = None):
        """Connect to the MCP server"""
        if mcp_url is None:
            mcp_url = os.getenv("MCP_SERVER_URL", "http://localhost:8000")

        # Initialize MCP client to connect to our todo operations server
        print(f"Connecting to MCP server at {mcp_url}")

    def send_message(self, message: str) -> str:
        """Send a message to the agent and get a response using Chat Completions API"""
        try:
            # 1. Append user message
            self.messages.append({"role": "user", "content": message})
            
            # 2. First API call
            response = openai_client.chat.completions.create(
                model=self.model,
                messages=self.messages,
                tools=self._get_tools(),
                tool_choice="auto"
            )
            
            response_message = response.choices[0].message
            
            # 3. Handle tool calls
            if response_message.tool_calls:
                # Append the assistant's message with tool calls to history
                self.messages.append(response_message)
                
                # Iterate through tool calls
                for tool_call in response_message.tool_calls:
                    function_name = tool_call.function.name
                    function_args = json.loads(tool_call.function.arguments)
                    
                    # Sanitize arguments (keep existing logic)
                    from ..utils.input_sanitizer import InputSanitizer
                    
                    if function_name == "add_todo":
                         if "content" in function_args:
                            function_args["content"] = InputSanitizer.sanitize_todo_content(function_args["content"])
                         result = self._handle_add_todo(function_args)
                         
                    elif function_name == "list_todos":
                         # Sanitize limit/offset
                         if "limit" in function_args:
                             try:
                                 limit = int(function_args["limit"])
                                 function_args["limit"] = max(1, min(100, limit))
                             except: function_args["limit"] = 50
                         result = self._handle_list_todos(function_args)
                         
                    elif function_name == "complete_todo":
                         if "todo_id" in function_args:
                            try: function_args["todo_id"] = InputSanitizer.validate_todo_id(function_args["todo_id"])
                            except: pass # Let handler deal with it or validation error
                         result = self._handle_complete_todo(function_args)
                         
                    elif function_name == "delete_todo":
                         if "todo_id" in function_args:
                            try: function_args["todo_id"] = InputSanitizer.validate_todo_id(function_args["todo_id"])
                            except: pass
                         result = self._handle_delete_todo(function_args)
                         
                    elif function_name == "update_todo":
                         if "todo_id" in function_args:
                            try: function_args["todo_id"] = InputSanitizer.validate_todo_id(function_args["todo_id"])
                            except: pass
                         if "content" in function_args:
                            function_args["content"] = InputSanitizer.sanitize_todo_content(function_args["content"])
                         result = self._handle_update_todo(function_args)
                    
                    else:
                        result = {"success": False, "message": f"Unknown function: {function_name}"}

                    # Determine what content to send back to the LLM
                    # We prefer the 'user_friendly_message' if available for the final response generation context
                    content_to_send = json.dumps(result)
                        
                    # Append tool output to history
                    self.messages.append({
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": function_name,
                        "content": content_to_send,
                    })

                # 4. Second API call (get final response)
                second_response = openai_client.chat.completions.create(
                    model=self.model,
                    messages=self.messages
                )
                final_response = second_response.choices[0].message.content
                self.messages.append({"role": "assistant", "content": final_response})
                return final_response

            else:
                # No tool calls, just normal response
                final_response = response_message.content
                self.messages.append({"role": "assistant", "content": final_response})
                return final_response

        except Exception as e:
            print(f"Error in send_message: {str(e)}")
            return f"An error occurred: {str(e)}"

    async def _call_mcp_server(self, operation: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Make an async call to the MCP server"""
        start_time = datetime.now()
        try:
            mcp_url = os.getenv("MCP_SERVER_URL", "http://localhost:8000")

            # Prepare the request to the MCP server
            # In a real MCP implementation, we would use the proper MCP protocol
            # For now, we'll make a direct call to our todo operations endpoint
            async with httpx.AsyncClient() as client:
                logger.info(f"Making MCP call to {operation} with params: {params}")

                if operation == "todo.add":
                    response = await client.post(f"{mcp_url}/add_todo", json=params)
                elif operation == "todo.list":
                    # Pass the parameters to the list endpoint
                    response = await client.post(f"{mcp_url}/list_todos", json=params)
                elif operation == "todo.complete":
                    response = await client.post(f"{mcp_url}/complete_todo", json=params)
                elif operation == "todo.delete":
                    response = await client.post(f"{mcp_url}/delete_todo", json=params)
                elif operation == "todo.update":
                    response = await client.post(f"{mcp_url}/update_todo", json=params)
                else:
                    error_msg = f"Unknown operation: {operation}"
                    logger.warning(error_msg)
                    return {"success": False, "message": error_msg}

                duration = (datetime.now() - start_time).total_seconds()

                if response.status_code == 200:
                    result = response.json()
                    log_mcp_call(operation, duration, True)
                    logger.info(f"MCP call {operation} completed successfully in {duration:.3f}s")
                    return result
                else:
                    error_msg = f"Error from MCP server: {response.text} (Status: {response.status_code})"
                    log_mcp_call(operation, duration, False)
                    logger.error(error_msg)
                    return {"success": False, "message": error_msg}
        except Exception as e:
            duration = (datetime.now() - start_time).total_seconds()
            log_mcp_call(operation, duration, False)
            log_error(e, {"operation": operation, "params": params})
            return {"success": False, "message": f"Error connecting to MCP server: {str(e)}"}

    def _handle_add_todo(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Handle the add_todo function call by connecting to MCP server"""
        try:
            logger.info(f"Calling MCP server to add todo: {args}")

            # Create an event loop to run the async function
            import asyncio
            try:
                loop = asyncio.get_event_loop()
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)

            # Call the MCP server
            result = loop.run_until_complete(self._call_mcp_server("todo.add", args))

            # If successful, generate user-friendly response
            if result.get("success") and "todo_id" in result:
                from ..utils.user_feedback import UserFeedback
                content = args.get("content", "a new todo")
                user_friendly_msg = UserFeedback.get_positive_response(
                    "add_todo",
                    {"content": content}
                )
                result["user_friendly_message"] = user_friendly_msg

            return result
        except Exception as e:
            logger.error(f"Error in _handle_add_todo: {e}")
            from ..services.error_handlers import handle_generic_error
            error_response = handle_generic_error(e)
            return {
                "success": False,
                "message": error_response.message,
                "user_friendly_message": error_response.user_friendly_message
            }

    def _handle_list_todos(self, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Handle the list_todos function call"""
        try:
            logger.info("Calling MCP server to list todos")

            # Use default parameters if none provided
            if params is None:
                params = {}

            # Create an event loop to run the async function
            import asyncio
            try:
                loop = asyncio.get_event_loop()
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)

            # Call the MCP server with parameters
            result = loop.run_until_complete(self._call_mcp_server("todo.list", params))

            # If successful, generate user-friendly response
            if result.get("success"):
                from ..utils.user_feedback import UserFeedback
                count = result.get("total_count", 0)
                user_friendly_msg = UserFeedback.get_positive_response(
                    "list_todos",
                    {"count": count}
                )
                result["user_friendly_message"] = user_friendly_msg

                # Format the todo list for better user experience
                if "todos" in result and result["todos"]:
                    formatted_list = UserFeedback.format_todo_list(result["todos"])
                    result["formatted_todo_list"] = formatted_list

            return result
        except Exception as e:
            logger.error(f"Error in _handle_list_todos: {e}")
            from ..services.error_handlers import handle_generic_error
            error_response = handle_generic_error(e)
            return {
                "success": False,
                "message": error_response.message,
                "user_friendly_message": error_response.user_friendly_message
            }

    def _handle_complete_todo(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Handle the complete_todo function call"""
        try:
            logger.info(f"Calling MCP server to complete todo: {args}")

            # Create an event loop to run the async function
            import asyncio
            try:
                loop = asyncio.get_event_loop()
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)

            # Call the MCP server
            result = loop.run_until_complete(self._call_mcp_server("todo.complete", args))

            # If successful, generate user-friendly response
            if result.get("success") and "todo" in result:
                from ..utils.user_feedback import UserFeedback
                content = result["todo"].get("content", "a todo")
                user_friendly_msg = UserFeedback.get_positive_response(
                    "complete_todo",
                    {"content": content}
                )
                result["user_friendly_message"] = user_friendly_msg

            return result
        except Exception as e:
            logger.error(f"Error in _handle_complete_todo: {e}")
            from ..services.error_handlers import handle_generic_error
            error_response = handle_generic_error(e)
            return {
                "success": False,
                "message": error_response.message,
                "user_friendly_message": error_response.user_friendly_message
            }

    def _handle_delete_todo(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Handle the delete_todo function call"""
        try:
            logger.info(f"Calling MCP server to delete todo: {args}")

            # Create an event loop to run the async function
            import asyncio
            try:
                loop = asyncio.get_event_loop()
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)

            # Call the MCP server
            result = loop.run_until_complete(self._call_mcp_server("todo.delete", args))

            # If successful, generate user-friendly response
            if result.get("success"):
                from ..utils.user_feedback import UserFeedback
                content = args.get("content", "a todo") or "a todo"  # Get content from args if available
                user_friendly_msg = UserFeedback.get_positive_response(
                    "delete_todo",
                    {"content": content}
                )
                result["user_friendly_message"] = user_friendly_msg

            return result
        except Exception as e:
            logger.error(f"Error in _handle_delete_todo: {e}")
            from ..services.error_handlers import handle_generic_error
            error_response = handle_generic_error(e)
            return {
                "success": False,
                "message": error_response.message,
                "user_friendly_message": error_response.user_friendly_message
            }

    def _handle_update_todo(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Handle the update_todo function call"""
        try:
            logger.info(f"Calling MCP server to update todo: {args}")

            # Create an event loop to run the async function
            import asyncio
            try:
                loop = asyncio.get_event_loop()
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)

            # Call the MCP server
            result = loop.run_until_complete(self._call_mcp_server("todo.update", args))

            # If successful, generate user-friendly response
            if result.get("success") and "todo" in result:
                from ..utils.user_feedback import UserFeedback
                original_content = args.get("content", "a todo")  # Get original content from args
                new_content = result["todo"].get("content", "a todo")
                user_friendly_msg = UserFeedback.get_positive_response(
                    "update_todo",
                    {"original_content": original_content, "new_content": new_content}
                )
                result["user_friendly_message"] = user_friendly_msg

            return result
        except Exception as e:
            logger.error(f"Error in _handle_update_todo: {e}")
            from ..services.error_handlers import handle_generic_error
            error_response = handle_generic_error(e)
            return {
                "success": False,
                "message": error_response.message,
                "user_friendly_message": error_response.user_friendly_message
            }


# Example usage
if __name__ == "__main__":
    agent = TodoAgent()
    print("Todo Agent initialized")

    # Example of sending a message
    response = agent.send_message("Add a new todo: Buy groceries")
    print(f"Response: {response}")