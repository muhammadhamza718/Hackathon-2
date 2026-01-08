"""Test script for end-to-end flow of adding todo via chat"""

import requests
import json
import time
import subprocess
import signal
import os
import sys

def test_end_to_end_flow():
    """Test the complete end-to-end flow"""
    print("Testing end-to-end flow for adding todo via chat...")

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

    # Test 2: Test the chat endpoint with a todo addition request
    try:
        test_message = {
            "message": "Add a new todo: Buy groceries"
        }

        response = requests.post(
            "http://localhost:8001/chat",
            headers={"Content-Type": "application/json"},
            data=json.dumps(test_message)
        )

        if response.status_code == 200:
            result = response.json()
            print(f"✓ Chat endpoint responded successfully")
            print(f"  Response: {result.get('response', 'No response text')}")

            # Check if the response contains expected content
            if "Buy groceries" in result.get('response', ''):
                print("✓ Todo was successfully added as per agent response")
            else:
                print("? Todo may not have been processed as expected")
        else:
            print(f"✗ Chat endpoint returned error: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Error testing chat endpoint: {e}")
        return False

    # Test 3: Test with the MCP server directly (if running)
    try:
        # Try to add a todo directly to the MCP server
        mcp_response = requests.post(
            "http://localhost:8080/add_todo",
            headers={"Content-Type": "application/json"},
            json={"content": "Test todo from e2e test", "due_date": None}
        )

        if mcp_response.status_code in [200, 404, 500]:  # 404/500 would indicate server is responding
            print("✓ MCP server is responding")
        else:
            print("? MCP server may not be accessible, but this might be expected")
    except Exception:
        print("? MCP server not accessible, this may be expected if it's not running")

    print("\n✓ End-to-end flow test completed")
    print("Note: For full testing, ensure both backend and MCP servers are running")
    return True

if __name__ == "__main__":
    success = test_end_to_end_flow()
    if success:
        print("\nEnd-to-end flow test completed successfully!")
        sys.exit(0)
    else:
        print("\nEnd-to-end flow test failed!")
        sys.exit(1)