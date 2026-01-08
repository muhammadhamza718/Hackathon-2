from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime
import uuid

class MessageBase(SQLModel):
    conversation_id: str = Field(foreign_key="conversation.id", index=True)
    role: str = Field(index=True) # user, assistant, system
    content: str
    user_id: Optional[str] = Field(default=None, index=True)

class Message(MessageBase, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationship to conversation
    conversation: Optional["Conversation"] = Relationship(back_populates="messages")

class MessageCreate(MessageBase):
    pass

class MessageRead(MessageBase):
    id: str
    created_at: datetime