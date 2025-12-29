import asyncio
import sys
import os

# Ensure backend directory is in python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlmodel import SQLModel
from db.session import async_engine
# Import models to register them
from models.user import User
from models.task import Task
from models.session import Session

async def init_db():
    print("Initializing Database...")
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    print("Database Initialized Successfully.")

if __name__ == "__main__":
    asyncio.run(init_db())
