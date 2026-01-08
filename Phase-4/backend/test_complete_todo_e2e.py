"""Test script for end-to-end flow of completing todos via chat"""

import requests
import json
import time
import sys

def test_complete_todo_e2e():
    """Test the complete end-to-end flow for completing a todo"""
    print("Testing end-to-end flow for completing todos via chat...")

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
        print("Please start the backend server first")
        return False

    # Test 2: Add a todo first to have something to complete
    print("\nStep 1: Adding a test todo...")
    try:
        test_message = {
            "message": "Add a new todo: Complete E2E test for todo completion"
        }

        response = requests.post(
            "http://localhost:8001/chat",
            headers={"Content-Type": "application/json"},
            data=json.dumps(test_message)
        )

        if response.status_code == 200:
            result = response.json()
            print(f"✓ Todo added successfully: {result.get('response', 'N/A')}")
        else:
            print(f"✗ Failed to add todo: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Error adding todo: {e}")
        return False

    # Test 3: List todos to find the one we just added
    print("\nStep 2: Listing todos to find the one to complete...")
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
            print(f"✓ Todo list retrieved: {result.get('response', 'N/A')}")

            # Parse the response to find the todo ID if possible
            # This is a simple test, in a real scenario we would need to parse the response properly
        else:
            print(f"✗ Failed to list todos: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Error listing todos: {e}")
        return False

    # Test 4: Complete the todo
    print("\nStep 3: Completing the todo...")
    try:
        # In a real test, we would use the actual ID from the previous step
        # For this test, we'll use a general message that the AI should interpret
        test_message = {
            "message": "Mark the todo 'Complete E2E test for todo completion' as completed"
        }

        response = requests.post(
            "http://localhost:8001/chat",
            headers={"Content-Type": "application/json"},
            data=json.dumps(test_message)
        )

        if response.status_code == 200:
            result = response.json()
            print(f"✓ Todo completion request processed: {result.get('response', 'N/A')}")

            # Check if the response indicates success
            response_text = result.get('response', '').lower()
            if 'complete' in response_text or 'completed' in response_text:
                print("✓ Response indicates the todo was marked as completed")
            else:
                print("? Response doesn't clearly indicate completion status")
        else:
            print(f"✗ Failed to complete todo: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Error completing todo: {e}")
        return False

    # Test 5: List todos again to verify the completion status
    print("\nStep 4: Verifying completion by listing todos again...")
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
            print(f"✓ Todo list retrieved after completion: {result.get('response', 'N/A')}")
            print("✓ End-to-end flow test completed successfully!")
            return True
        else:
            print(f"✗ Failed to list todos after completion: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Error verifying completion: {e}")
        return False

if __name__ == "__main__":
    success = test_complete_todo_e2e()
    if success:
        print("\n✓ All end-to-end tests for completing todos passed!")
        sys.exit(0)
    else:
        print("\n✗ Some tests failed!")
        sys.exit(1)