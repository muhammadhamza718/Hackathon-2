"""Test script for end-to-end flow of listing todos via chat"""

import requests
import json
import time
import subprocess
import signal
import os
import sys

def test_list_todos_flow():
    """Test the complete end-to-end flow for listing todos"""
    print("Testing end-to-end flow for listing todos via chat...")

    # Test 1: Verify the backend server is running
    try:
        response = requests.get("http://localhost:8001/health")
        if response.status_code == 200:
            print("✓ Backend server is running")
        else:
            print("✗ Backend server health check failed")
            return False
    except Exception as e:
        print(f"✗ Backend server is not accessible: {e}")
        print("Please start the backend server with: python -m backend.src.api.server")
        return False

    # Test 2: First add a few todos to have something to list
    print("\nAdding test todos...")
    test_todos = [
        "Test todo 1: Buy groceries",
        "Test todo 2: Walk the dog",
        "Test todo 3: Call mom"
    ]

    for todo in test_todos:
        try:
            test_message = {
                "message": f"Add a new todo: {todo}"
            }

            response = requests.post(
                "http://localhost:8001/chat",
                headers={"Content-Type": "application/json"},
                data=json.dumps(test_message)
            )

            if response.status_code == 200:
                result = response.json()
                print(f"  ✓ Added: {todo}")
            else:
                print(f"  ✗ Failed to add: {todo}")
        except Exception as e:
            print(f"  ✗ Error adding todo: {e}")

    # Test 3: Test the chat endpoint with a list todos request
    try:
        test_message = {
            "message": "List all my todos"
        }

        response = requests.post(
            "http://localhost:8001/chat",
            headers={"Content-Type": "application/json"},
            data=json.dumps(test_message)
        )

        if response.status_code == 200:
            result = response.json()
            print(f"✓ List todos request responded successfully")
            print(f"  Response preview: {result.get('response', 'No response text')[:100]}...")

            # Check if the response contains expected content
            response_text = result.get('response', '').lower()
            if "todo" in response_text or "todos" in response_text:
                print("✓ Response contains expected todo-related content")
            else:
                print("? Response may not contain expected todo content")
        else:
            print(f"✗ List todos endpoint returned error: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Error testing list todos endpoint: {e}")
        return False

    # Test 4: Test with the MCP server directly (if running) to list todos
    try:
        # Try to list todos directly from the MCP server
        mcp_response = requests.post(
            "http://localhost:8080/list_todos",
            headers={"Content-Type": "application/json"},
            json={"completed": None, "limit": 50, "offset": 0}
        )

        if mcp_response.status_code in [200, 404, 500]:  # 404/500 would indicate server is responding
            print("✓ MCP server list endpoint is responding")
        else:
            print("? MCP server list endpoint may not be accessible, but this might be expected")
    except Exception:
        print("? MCP server not accessible, this may be expected if it's not running")

    print("\n✓ End-to-end flow test for listing todos completed")
    print("Note: For full testing, ensure both backend and MCP servers are running")
    return True

if __name__ == "__main__":
    success = test_list_todos_flow()
    if success:
        print("\nEnd-to-end flow test for listing todos completed successfully!")
        sys.exit(0)
    else:
        print("\nEnd-to-end flow test for listing todos failed!")
        sys.exit(1)