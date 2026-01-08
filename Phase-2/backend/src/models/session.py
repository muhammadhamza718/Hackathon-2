from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime


class UserSessionBase(SQLModel):
    user_id: str = Field(min_length=1, max_length=100)
    session_token: str = Field(min_length=1, max_length=200)
    expires_at: datetime


class UserSession(UserSessionBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(min_length=1, max_length=100, index=True)  # Index for user lookups
    session_token: str = Field(min_length=1, max_length=200, unique=True, index=True)  # Index for session token lookups
    expires_at: datetime = Field(index=True)  # Index for expiration checks
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)  # Index for sorting by creation date
    updated_at: datetime = Field(default_factory=datetime.utcnow, index=True)  # Index for sorting by update date
    is_active: bool = Field(default=True, index=True)  # Index for filtering active sessions


class UserSessionCreate(UserSessionBase):
    pass


class UserSessionUpdate(SQLModel):
    session_token: Optional[str] = Field(default=None, min_length=1, max_length=200)
    expires_at: Optional[datetime] = Field(default=None)
    is_active: Optional[bool] = Field(default=None)


class UserSessionRead(UserSessionBase):
    id: int
    created_at: datetime
    updated_at: datetime
    is_active: bool