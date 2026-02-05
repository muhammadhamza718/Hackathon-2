import logging
import os
from openai import AsyncOpenAI
from agents import Agent, set_tracing_disabled, OpenAIChatCompletionsModel
from dotenv import load_dotenv

# Load environment variables BEFORE any local imports that create DB engines
load_dotenv()


# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Disable OpenAI tracing
set_tracing_disabled(True)


def init_llm_client() -> AsyncOpenAI:
    """Initialize AsyncOpenAI client for Gemini"""
    api_key = os.getenv("GEMINI_API_KEY")
    base_url = "https://generativelanguage.googleapis.com/v1beta/openai/"

    if not api_key or api_key.startswith("YOUR_"):
        logger.error("❌ No valid GEMINI_API_KEY found!")
        raise ValueError("GEMINI_API_KEY environment variable is required")

    logger.info(f"✅ Using GEMINI_API_KEY (starts with: {api_key[:4]}...)")
    logger.info(f"Initializing AsyncOpenAI client with base_url: {base_url}")

    return AsyncOpenAI(api_key=api_key, base_url=base_url)


# ===== LLM SETUP =====
GEMINI_MODEL_NAME = "gemini-2.5-flash"
_client = init_llm_client()
GEMINI_MODEL = OpenAIChatCompletionsModel(
    model=GEMINI_MODEL_NAME,
    openai_client=_client
)

# ===== AGENT CREATION =====


def create_todo_agent(tools: list = None) -> Agent:
    """
    Create a todo agent with Gemini model.
    The tools should be provided by the MCP client.
    """

    instructions = """You are a helpful AI assistant for managing todo lists.

    CRITICAL: ALWAYS respond in English. Do not use German or any other language filler phrases.

You can help users:
- Add new tasks
- List tasks (optionally filtered by completion status)
- Mark tasks as complete
- Delete tasks
- Update task content or status

IMPORTANT GUIDELINES:
1. Always use the provided tools (add_task, list_tasks, etc.) to interact with the database.
2. If a user asks to see their items, use 'list_tasks'.
3. Always include the 'id' of the task when showing a list so the user can easily reference them for updates/deletion.
4. Be conversational, friendly, and use emojis (✅, 📋, 🗑️).
5. Always confirm when an action has been successfully completed.
"""

    agent = Agent(
        name="Todo Assistant",
        instructions=instructions,
        model=GEMINI_MODEL,
        tools=tools or []
    )

    logger.info(f"✅ Todo agent created with {len(tools or [])} tools")
    return agent
