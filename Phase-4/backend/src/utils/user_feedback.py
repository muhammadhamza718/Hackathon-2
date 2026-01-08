"""User feedback and response utilities for the Todo Chatbot"""
from typing import Dict, Any, Optional
import re


class UserFeedback:
    """Provides user-friendly responses and feedback for various scenarios"""

    @staticmethod
    def get_positive_response(action: str, details: Optional[Dict[str, Any]] = None) -> str:
        """Generate positive feedback for successful actions"""
        responses = {
            "add_todo": [
                "I've added '{content}' to your todo list.",
                "Got it! I've added '{content}' to your todos.",
                "Your todo '{content}' has been added successfully."
            ],
            "list_todos": [
                "Here are your todos: {count} items found.",
                "I found {count} todos for you.",
                "Your current todos: {count} items."
            ],
            "complete_todo": [
                "Great job! I've marked '{content}' as completed.",
                "Nice! '{content}' has been marked as completed.",
                "I've updated '{content}' to completed status."
            ],
            "delete_todo": [
                "I've removed '{content}' from your todo list.",
                "Got it! '{content}' has been deleted.",
                "I've removed '{content}' from your todos."
            ],
            "update_todo": [
                "I've updated '{original_content}' to '{new_content}'.",
                "Your todo '{original_content}' has been updated.",
                "Changes saved for '{original_content}'."
            ]
        }

        if action in responses:
            response_template = responses[action][0]  # Use first response as default
            if details:
                try:
                    return response_template.format(**details)
                except KeyError:
                    # If formatting fails, return the template as-is
                    return response_template
            return response_template

        return "Action completed successfully."

    @staticmethod
    def get_understanding_response(user_input: str) -> str:
        """Generate a response showing the system understood the user's request"""
        understanding_phrases = [
            "I understand you want to {action}.",
            "Okay, I'll help you {action}.",
            "Got it, I'll {action} for you.",
            "I'll take care of {action} for you."
        ]

        # Simple action detection
        action = "help with your request"
        if "add" in user_input.lower() or "create" in user_input.lower():
            action = "add a todo"
        elif "list" in user_input.lower() or "show" in user_input.lower() or "see" in user_input.lower():
            action = "list your todos"
        elif "complete" in user_input.lower() or "done" in user_input.lower() or "finish" in user_input.lower():
            action = "mark a todo as completed"
        elif "delete" in user_input.lower() or "remove" in user_input.lower():
            action = "delete a todo"
        elif "update" in user_input.lower() or "change" in user_input.lower():
            action = "update a todo"

        return understanding_phrases[0].format(action=action)

    @staticmethod
    def get_help_response() -> str:
        """Provide help information to the user"""
        return (
            "I can help you manage your todos! You can ask me to:\n"
            "- Add a new todo: 'Add buy groceries'\n"
            "- List your todos: 'Show my todos' or 'What are my todos?'\n"
            "- Mark a todo as completed: 'Mark todo 1 as completed'\n"
            "- Delete a todo: 'Delete todo 1' or 'Remove todo 1'\n"
            "- Update a todo: 'Update todo 1 to buy vegetables'\n\n"
            "Just tell me what you'd like to do!"
        )

    @staticmethod
    def get_confused_response() -> str:
        """Response when the system doesn't understand the user's request"""
        return (
            "I'm not sure I understood that. Could you please rephrase your request? "
            "You can ask me to add, list, complete, delete, or update your todos."
        )

    @staticmethod
    def get_error_recovery_suggestions(error_type: str) -> str:
        """Provide suggestions for common errors"""
        suggestions = {
            "todo_not_found": "Please check the todo ID and try again. You can list your todos to see available IDs.",
            "validation_error": "Please check the information you provided and try again.",
            "database_error": "I'm having trouble accessing your todos. Please try again in a moment.",
            "mcp_error": "I'm having trouble connecting to the todo service. Please try again."
        }

        return suggestions.get(error_type, "Please try again or ask for help if the problem persists.")

    @staticmethod
    def personalize_response(response: str, user_context: Optional[Dict[str, Any]] = None) -> str:
        """Add personalization to responses based on user context"""
        if user_context and user_context.get("time_of_day"):
            time_greeting = ""
            if "morning" in user_context["time_of_day"].lower():
                time_greeting = "Good morning! "
            elif "afternoon" in user_context["time_of_day"].lower():
                time_greeting = "Good afternoon! "
            elif "evening" in user_context["time_of_day"].lower():
                time_greeting = "Good evening! "
            elif "night" in user_context["time_of_day"].lower():
                time_greeting = "Good night! "

            if time_greeting:
                return time_greeting + response

        return response

    @staticmethod
    def format_todo_list(todos: list) -> str:
        """Format a list of todos for user display"""
        if not todos:
            return "You don't have any todos right now."

        formatted = "Here are your todos:\n"
        for i, todo in enumerate(todos, 1):
            status = "✓" if todo.get("completed", False) else "○"
            due_date = f" (due: {todo.get('due_date', 'no date')})" if todo.get("due_date") else ""
            formatted += f"{i}. [{status}] {todo.get('content', 'No content')}{due_date}\n"

        return formatted.strip()

    @staticmethod
    def format_todo_item(todo: Dict[str, Any]) -> str:
        """Format a single todo item for user display"""
        status = "✓" if todo.get("completed", False) else "○"
        due_date = f" (due: {todo.get('due_date', 'no date')})" if todo.get("due_date") else ""
        return f"[{status}] {todo.get('content', 'No content')}{due_date}"