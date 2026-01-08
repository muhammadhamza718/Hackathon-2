import requests
import uuid
from datetime import datetime, timedelta, timezone
from sqlmodel import Session, select
import os
from dotenv import load_dotenv
import sys
from pathlib import Path

# Load env for database URL
load_dotenv()

# Add current dir to path for imports
sys.path.append(str(Path(__file__).parent))
from src.models.database import sync_engine
from models.user import User
from models.session import Session as DbSession

def verify_chatkit():
    print("🚀 Starting ChatKit Authentication Verification...")
    
    # 1. Setup Test User and Session
    try:
        with Session(sync_engine) as session:
            # Check for demo user
            user = session.exec(select(User).where(User.email == "verification_test@example.com")).first()
            if not user:
                print("Creating test user...")
                user = User(id=str(uuid.uuid4()), email="verification_test@example.com", name="Verifier")
                session.add(user)
                session.commit()
                session.refresh(user)
            
            # Create a fresh session token
            test_token = f"test_token_{uuid.uuid4().hex[:8]}"
            new_session = DbSession(
                id=str(uuid.uuid4()),
                userId=user.id,
                token=test_token,
                expiresAt=datetime.now(timezone.utc) + timedelta(hours=1)
            )
            session.add(new_session)
            session.commit()
            print(f"✅ Created test session for User: {user.id}")
            print(f"🔑 Token: {test_token}")
    except Exception as e:
        print(f"❌ Database error: {e}")
        return

    # 2. Call ChatKit Handshake
    url = "http://localhost:8000/chatkit"
    headers = {
        "Authorization": f"Bearer {test_token}",
        "Content-Type": "application/json"
    }
    # ChatKit Handshake body
    payload = {
        "kind": "handshake",
        "domainKey": "domain_pk_694e660b27cc8194af36166984c678920dffab26d4b3cd54"
    }
    
    print(f"Sending POST to {url} with auth header...")
    try:
        # Use a timeout of 10s
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        print(f"Status Code: {response.status_code}")
        
        # Handshake usually returns 200 or 201
        if response.status_code in [200, 201]:
            print("🎉 SUCCESS: Handshake accepted!")
            print(f"Response: {response.text[:200]}...")
        elif response.status_code == 401:
            print("❌ FAILURE: Unauthorized (401)")
            print(f"Detail: {response.text}")
        else:
            print(f"❓ Unexpected status code: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error during request: {e}")

if __name__ == "__main__":
    verify_chatkit()
