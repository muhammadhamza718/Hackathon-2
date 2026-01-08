from dotenv import load_dotenv

# Load environment variables BEFORE any operations that need them
load_dotenv()

from sqlmodel import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from typing import AsyncGenerator
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://user:password@localhost:5432/todoapp")

# Robust URL handling
from urllib.parse import urlparse, parse_qs, urlunparse

if DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)

parsed = urlparse(DATABASE_URL)
query_params = parse_qs(parsed.query)

# Cleaned URL without query params
DATABASE_URL = urlunparse(parsed._replace(query=""))

# connection args
connect_args = {}

# Handle SSL explicitly
if "sslmode" in query_params:
    sslrequest = query_params["sslmode"][0]
    if sslrequest == "require":
        connect_args["ssl"] = "require"

# Create async engine with robust args
async_engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    connect_args=connect_args,
    pool_pre_ping=True
)

# Create async session
AsyncSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session