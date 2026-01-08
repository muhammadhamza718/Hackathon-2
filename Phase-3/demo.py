"""Simple demonstration of the end-to-end flow"""

import asyncio
from backend.src.agents.agent import TodoAgent

async def demo_end_to_end():
    """Demonstrate the end-to-end functionality"""
    print("Initializing Todo Agent...")

    # Create the agent
    agent = TodoAgent()

    print("Agent initialized. Connecting to MCP server...")
    # Connect to MCP server
    await agent.connect_to_mcp_server()

    print("Connected to MCP server. Testing functionality...")

    # Test adding a todo
    print("\n1. Adding a todo...")
    response = agent.send_message("Add a new todo: Buy groceries")
    print(f"Response: {response}")

    # Test listing todos
    print("\n2. Listing todos...")
    response = agent.send_message("List all my todos")
    print(f"Response: {response}")

    print("\nEnd-to-end demonstration completed!")

if __name__ == "__main__":
    asyncio.run(demo_end_to_end())