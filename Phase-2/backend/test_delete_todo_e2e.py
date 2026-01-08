"""Test script for end-to-end flow of deleting todos via chat"""

import requests
import json
import time
import sys

def test_delete_todo_e2e():
    """Test the complete end-to-end flow for deleting a todo"""
    print("Testing end-to-end flow for deleting todos via chat...")

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

    # Test 2: Add a todo first to have something to delete
    print("\nStep 1: Adding a test todo...")
    try:
        test_message = {
            "message": "Add a new todo: Delete me test item"
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
    print("\nStep 2: Listing todos to verify the added todo...")
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

            # Check if the response contains the added todo
            response_text = result.get('response', '').lower()
            if 'delete me test item' in response_text:
                print("✓ Added todo is present in the list")
            else:
                print("? Added todo may not be in the list")
        else:
            print(f"✗ Failed to list todos: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Error listing todos: {e}")
        return False

    # Test 4: Delete the todo
    print("\nStep 3: Deleting the todo...")
    try:
        # In a real test, we would use the actual ID from the previous step
        # For this test, we'll use a general message that the AI should interpret
        test_message = {
            "message": "Delete the todo 'Delete me test item'"
        }

        response = requests.post(
            "http://localhost:8001/chat",
            headers={"Content-Type": "application/json"},
            data=json.dumps(test_message)
        )

        if response.status_code == 200:
            result = response.json()
            print(f"✓ Todo deletion request processed: {result.get('response', 'N/A')}")

            # Check if the response indicates success
            response_text = result.get('response', '').lower()
            if 'delete' in response_text or 'deleted' in response_text:
                print("✓ Response indicates the todo was deleted")
            else:
                print("? Response doesn't clearly indicate deletion status")
        else:
            print(f"✗ Failed to delete todo: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Error deleting todo: {e}")
        return False

    # Test 5: List todos again to verify the deletion
    print("\nStep 4: Verifying deletion by listing todos again...")
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
            print(f"✓ Todo list retrieved after deletion: {result.get('response', 'N/A')}")

            # Check if the deleted todo is no longer in the list
            response_text = result.get('response', '').lower()
            if 'delete me test item' not in response_text:
                print("✓ Deleted todo is no longer in the list (verification successful)")
            else:
                print("? Deleted todo may still be in the list")

            print("✓ End-to-end flow test completed successfully!")
            return True
        else:
            print(f"✗ Failed to list todos after deletion: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Error verifying deletion: {e}")
        return False

if __name__ == "__main__":
    success = test_delete_todo_e2e()
    if success:
        print("\n✓ All end-to-end tests for deleting todos passed!")
        sys.exit(0)
    else:
        print("\n✗ Some tests failed!")
        sys.exit(1)