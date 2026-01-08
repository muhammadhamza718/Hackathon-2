import asyncio
import sys
import os

# Ensure backend directory is in python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import text
from db.session import async_engine

async def force_admin(user_id):
    print(f"Forcing admin for: {user_id}")
    async with async_engine.begin() as conn: # begin() commits on exit
        # Check before
        res = await conn.execute(text('SELECT role FROM "user" WHERE id = :uid'), {"uid": user_id})
        prev = res.scalar()
        print(f"Previous Role: {prev}")

        # Update
        print("Executing UPDATE...")
        await conn.execute(text('UPDATE "user" SET role = \'admin\' WHERE id = :uid'), {"uid": user_id})
        
        # Check after (within same transaction might show update, but real proof is after commit)
        pass

    # Verify after commit
    async with async_engine.connect() as conn:
         res = await conn.execute(text('SELECT role FROM "user" WHERE id = :uid'), {"uid": user_id})
         new_role = res.scalar()
         print(f"New Role: '{new_role}'")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python force_admin.py <user_id>")
        sys.exit(1)
    asyncio.run(force_admin(sys.argv[1]))
