from dotenv import load_dotenv

# Load environment variables BEFORE creating engines that need them
load_dotenv()

from sqlmodel import create_engine, Session
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import os
from typing import Generator
from sqlalchemy.pool import QueuePool


# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/dbname")


# Synchronous engine with connection pooling for regular operations
sync_engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
    pool_recycle=300
)

# Async engine with connection pooling for async operations
ASYNC_DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://").replace("postgres://", "postgresql+asyncpg://")

# Async engine creation
async_engine = create_async_engine(
    ASYNC_DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=300,
    echo=False
)

# Session makers
AsyncSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

SyncSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=sync_engine,
    expire_on_commit=False
)


def get_sync_session() -> Generator[Session, None, None]:
    """Get a synchronous database session."""
    session = SyncSessionLocal()
    try:
        yield session
    finally:
        session.close()


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Get an asynchronous database session."""
    async with AsyncSessionLocal() as session:
        yield session
        await session.close()


def create_db_and_tables():
    """Create database tables and indexes."""
    from models.user import User
    from models.session import Session
    from models.task import Task
    from .conversation import Conversation
    from .message import Message
    from sqlmodel import SQLModel

    # Create all tables with indexes
    SQLModel.metadata.create_all(bind=sync_engine)


def run_migrations():
    """Run database migrations to ensure indexes are up to date."""
    from models.task import Task
    from .conversation import Conversation
    from .message import Message
    from sqlmodel import SQLModel
    from sqlalchemy import inspect

    # Get database inspector
    inspector = inspect(sync_engine)

    # Create tables and indexes
    SQLModel.metadata.create_all(bind=sync_engine)

    # Log index information for optimization verification
    for table_name in ['task', 'conversation', 'message']:
        if table_name in inspector.get_table_names():
            indexes = inspector.get_indexes(table_name)
            print(f"Indexes for {table_name}: {[idx['name'] for idx in indexes]}")