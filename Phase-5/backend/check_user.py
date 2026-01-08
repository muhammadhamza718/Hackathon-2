import asyncio
import os
from sqlmodel import select
from models.user import User
from db.session import get_async_session
from dotenv import load_dotenv

load_dotenv()

async def check_user(email: str):
    print(f"Checking for user: {email}...")
    try:
        async for session in get_async_session():
            statement = select(User).where(User.email == email)
            result = await session.execute(statement)
            user = result.scalars().first()
            if user:
                print(f"✅ User FOUND: {user.email} (Role: {user.role})")
            else:
                print("❌ User NOT FOUND. Please sign up first.")
            return
    except Exception as e:
        print(f"❌ Error checking user: {e}")

if __name__ == "__main__":
    asyncio.run(check_user("mhamza77188@gmail.com"))
