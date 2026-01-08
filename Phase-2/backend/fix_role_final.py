import asyncio
import sys
import os

# Ensure backend directory is in python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import text
from db.session import async_engine

async def main():
    user_id = "lNKmaiMTiGexTDFFBbjx0pGqxtw2W78K"
    print(f"Connecting to DB for User: {user_id}")
    try:
        async with async_engine.begin() as conn:
            # 1. READ
            print("Reading Role...")
            res = await conn.execute(text('SELECT role FROM "user" WHERE id = :uid'), {"uid": user_id})
            role = res.scalar()
            print(f"CURRENT ROLE: {role}")
            
            # 2. UPDATE (if not admin)
            if role != 'admin':
                print("Role is not admin. Updating...")
                await conn.execute(text('UPDATE "user" SET role = \'admin\' WHERE id = :uid'), {"uid": user_id})
                print("UPDATE EXECUTED.")
            else:
                print("Role is already admin. No changes needed.")
                
    except Exception as e:
        print(f"ERROR: {e}")
    finally:
        await async_engine.dispose()
        print("Engine disposed.")

if __name__ == "__main__":
    asyncio.run(main())
