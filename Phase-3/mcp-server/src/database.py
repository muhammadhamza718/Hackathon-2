from sqlmodel import create_engine, Session
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from contextlib import asynccontextmanager
import os
from typing import Generator
from .config import MCPConfig
from sqlalchemy.pool import QueuePool


# Synchronous engine with connection pooling for regular operations
sync_engine = create_engine(
    MCPConfig.DATABASE_URL,
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
    pool_recycle=300
)

# Async engine with connection pooling for async operations
async_engine = create_async_engine(
    MCPConfig.DATABASE_URL,
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
    pool_recycle=300
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
    """Create database tables."""
    # Import models to register them with SQLModel
    from backend.src.models.todo import Todo
    from backend.src.models.session import UserSession
    from backend.src.models.message import ChatMessage
    from sqlmodel import SQLModel

    SQLModel.metadata.create_all(bind=sync_engine)