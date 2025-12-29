import asyncio
import sys
import os

# Ensure backend directory is in python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import text
from db.session import async_engine

async def check_role(user_id):
    print(f"Checking role for user: {user_id}")
    async with async_engine.connect() as conn:
        result = await conn.execute(text('SELECT id, email, role FROM "user" WHERE id = :uid'), {"uid": user_id})
        user = result.fetchone()
        if user:
            print(f"Found User: {user.email}")
            print(f"Role: '{user.role}'") # Quote it to see if there are spaces
        else:
            print("User not found.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python check_role.py <user_id>")
        sys.exit(1)
    asyncio.run(check_role(sys.argv[1]))
