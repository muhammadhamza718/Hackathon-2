import httpx
import json

def test_chatkit():
    try:
        # ChatKit usually starts with a handshake or a session request
        # We'll just send an empty JSON to see how it responds
        response = httpx.post("http://127.0.0.1:8000/chatkit", json={}, timeout=10)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_chatkit()
