from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class Session(SQLModel, table=True):
    __tablename__ = "session"  # Must match Better Auth's table name

    id: str = Field(primary_key=True)
    userId: str = Field(foreign_key="user.id")
    token: str = Field(index=True)
    expiresAt: datetime
    ipAddress: Optional[str] = None
    userAgent: Optional[str] = None
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    updatedAt: datetime = Field(default_factory=datetime.utcnow)
