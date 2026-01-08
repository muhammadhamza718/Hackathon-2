from typing import Any, Optional, List
from datetime import datetime
from sqlmodel import Session, select, desc
from chatkit.store import Store, ThreadMetadata, ThreadItem, Page
from src.models.database import sync_engine
from src.models.conversation import Conversation
from src.models.message import Message
import logging

logger = logging.getLogger(__name__)

class SqlModelStore(Store[dict[str, Any]]):
    """Database-backed store for ChatKit using SQLModel"""

    def _get_user_id(self, context: dict[str, Any]) -> str:
        # Extract user_id from context, default to anonymous if not found
        # In a real app, this would come from the auth middleware
        return context.get("user_id") or context.get("request", {}).scope.get("user_id") or "anonymous"

    async def load_thread(self, thread_id: str, context: dict[str, Any]) -> Optional[ThreadMetadata]:
        user_id = self._get_user_id(context)
        with Session(sync_engine) as session:
            conv = session.exec(
                select(Conversation).where(Conversation.id == thread_id, Conversation.user_id == user_id)
            ).first()
            if not conv:
                return None
            return ThreadMetadata(
                id=conv.id,
                created_at=int(conv.created_at.timestamp() * 1000),
                metadata={"user_id": conv.user_id, "title": conv.title}
            )

    async def load_threads(
        self, 
        limit: int, 
        after: Optional[str] = None,
        order: str = "desc",
        context: dict[str, Any] = None
    ) -> Page[ThreadMetadata]:
        user_id = self._get_user_id(context or {})
        with Session(sync_engine) as session:
            statement = select(Conversation).where(Conversation.user_id == user_id)
            if order == "desc":
                statement = statement.order_by(desc(Conversation.updated_at))
            else:
                statement = statement.order_by(Conversation.updated_at)
            
            statement = statement.limit(limit)
            results = session.exec(statement).all()
            
            threads = [
                ThreadMetadata(
                    id=c.id,
                    created_at=int(c.created_at.timestamp() * 1000),
                    metadata={"user_id": c.user_id, "title": c.title}
                ) for c in results
            ]
            
            return Page(data=threads, after=None)

    async def save_thread(self, thread: ThreadMetadata, context: dict[str, Any]) -> None:
        user_id = self._get_user_id(context)
        title = thread.metadata.get("title", "New Chat")
        
        with Session(sync_engine) as session:
            # Enforce user isolation on update
            conv = session.exec(
                select(Conversation).where(Conversation.id == thread.id, Conversation.user_id == user_id)
            ).first()
            
            if conv:
                conv.updated_at = datetime.utcnow()
                conv.title = title
            else:
                conv = Conversation(
                    id=thread.id,
                    user_id=user_id,
                    title=title,
                    created_at=thread.created_at if isinstance(thread.created_at, datetime) else datetime.fromtimestamp(thread.created_at / 1000)
                )
            session.add(conv)
            session.commit()

    async def delete_thread(self, thread_id: str, context: dict[str, Any]) -> None:
        user_id = self._get_user_id(context)
        with Session(sync_engine) as session:
            conv = session.exec(
                select(Conversation).where(Conversation.id == thread_id, Conversation.user_id == user_id)
            ).first()
            
            if conv:
                # Delete associated messages first
                statement = select(Message).where(Message.conversation_id == thread_id)
                msgs = session.exec(statement).all()
                for m in msgs:
                    session.delete(m)
                session.delete(conv)
                session.commit()

    async def load_thread_items(
        self,
        thread_id: str,
        after: Optional[str] = None,
        limit: int = 20,
        order: str = "desc",
        context: dict[str, Any] = None
    ) -> Page[ThreadItem]:
        user_id = self._get_user_id(context or {})
        with Session(sync_engine) as session:
            # Verify the thread belongs to the user
            conv = session.exec(
                select(Conversation).where(Conversation.id == thread_id, Conversation.user_id == user_id)
            ).first()
            
            if not conv:
                return Page(data=[], after=None)
                
            statement = select(Message).where(Message.conversation_id == thread_id)
            
            if order == "desc":
                statement = statement.order_by(desc(Message.created_at))
            else:
                statement = statement.order_by(Message.created_at)
                
            statement = statement.limit(limit)
            results = session.exec(statement).all()
            
            items = []
            for m in results:
                created_at = m.created_at
                if m.role == "user":
                    from chatkit.types import UserMessageItem, UserMessageTextContent, InferenceOptions
                    items.append(UserMessageItem(
                        id=m.id,
                        thread_id=m.conversation_id,
                        created_at=created_at,
                        content=[UserMessageTextContent(text=m.content)],
                        inference_options=InferenceOptions()
                    ))
                else:
                    from chatkit.types import AssistantMessageItem, AssistantMessageContent
                    items.append(AssistantMessageItem(
                        id=m.id,
                        thread_id=m.conversation_id,
                        created_at=created_at,
                        content=[AssistantMessageContent(text=m.content)]
                    ))
            
            return Page(data=items, after=None)

    async def add_thread_item(self, thread_id: str, item: ThreadItem, context: dict[str, Any]) -> None:
        await self.save_item(thread_id, item, context)

    def _extract_text(self, item: ThreadItem) -> str:
        if hasattr(item, "text"):
            return item.text
        if hasattr(item, "content") and isinstance(item.content, list):
            texts = []
            for part in item.content:
                if hasattr(part, "text"):
                    texts.append(part.text)
            return "\n".join(texts)
        return ""

    async def save_item(self, thread_id: str, item: ThreadItem, context: dict[str, Any]) -> None:
        user_id = self._get_user_id(context)
        text = self._extract_text(item)
        role = "user" if item.type == "user_message" else "assistant" if item.type == "assistant_message" else str(item.type)
        
        with Session(sync_engine) as session:
            # Verify the thread belongs to the user
            conv = session.exec(
                select(Conversation).where(Conversation.id == thread_id, Conversation.user_id == user_id)
            ).first()
            
            if not conv:
                logger.warning(f"Attempted to save item to thread {thread_id} that doesn't belong to user {user_id}")
                return

            msg = session.get(Message, item.id)
            if msg:
                # Enforce user isolation on update
                if msg.user_id and msg.user_id != user_id:
                     logger.warning(f"User {user_id} attempted to update message {item.id} belonging to {msg.user_id}")
                     return
                msg.content = text
            else:
                msg = Message(
                    id=item.id,
                    conversation_id=thread_id,
                    role=role,
                    content=text,
                    user_id=user_id,
                    created_at=item.created_at if isinstance(item.created_at, datetime) else datetime.fromtimestamp(item.created_at / 1000)
                )
            session.add(msg)
            
            # Update conversation timestamp
            conv.updated_at = datetime.utcnow()
            session.add(conv)
                
            session.commit()

    async def load_item(self, thread_id: str, item_id: str, context: dict[str, Any]) -> ThreadItem:
        user_id = self._get_user_id(context)
        with Session(sync_engine) as session:
            msg = session.exec(
                select(Message).where(Message.id == item_id, Message.conversation_id == thread_id, Message.user_id == user_id)
            ).first()
            
            if not msg:
                raise KeyError(f"Item {item_id} not found or access denied")
            
            # Note: The mapping here might need fix depending on how ThreadItem is used (generic vs specific)
            # For simplicity, returning a generic item if required, but load_thread_items shows more specific way
            # Usually ChatKit uses specific types
            return ThreadItem(
                id=msg.id,
                created_at=int(msg.created_at.timestamp() * 1000),
                role=msg.role,
                text=msg.content
            )

    async def delete_thread_item(self, thread_id: str, item_id: str, context: dict[str, Any]) -> None:
        user_id = self._get_user_id(context)
        with Session(sync_engine) as session:
            msg = session.exec(
                select(Message).where(Message.id == item_id, Message.conversation_id == thread_id, Message.user_id == user_id)
            ).first()
            if msg:
                session.delete(msg)
                session.commit()

    # Attachment stubs to satisfy abstract class requirements
    async def save_attachment(self, attachment: Any, context: dict[str, Any]) -> None:
        pass

    async def load_attachment(self, attachment_id: str, context: dict[str, Any]) -> Any:
        raise KeyError(f"Attachment {attachment_id} not found")

    async def delete_attachment(self, attachment_id: str, context: dict[str, Any]) -> None:
        pass
