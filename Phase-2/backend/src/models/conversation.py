from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
import uuid

class ConversationBase(SQLModel):
    user_id: str = Field(index=True)
    title: Optional[str] = Field(default="New Chat")

class Conversation(ConversationBase, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationship to messages
    messages: List["Message"] = Relationship(back_populates="conversation")

class ConversationCreate(ConversationBase):
    pass

class ConversationRead(ConversationBase):
    id: str
    created_at: datetime
    updated_at: datetime
