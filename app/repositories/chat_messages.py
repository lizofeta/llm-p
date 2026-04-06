# Доступ к таблице чатов

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete

from app.db.models import ChatMessage

class ChatMessagesStorage:
    def __init__(self, db: AsyncSession):
        self._db = db 
    
    async def add_message(
            self, 
            user_id: int, 
            role: str,
            content: str
            ) -> ChatMessage:
        message = ChatMessage(
            user_id=user_id,
            role=role,
            content=content
        )
        self._db.add(message)
        await self._db.commit()
        await self._db.refresh(message)
        return message
    
    async def show_last_n_messages(
            self, 
            user_id: int, 
            limit: int
            ) -> list[ChatMessage]:
        result = await self._db.scalars(select(ChatMessage)
                                .where(ChatMessage.user_id == user_id)
                                .order_by(ChatMessage.created_at.desc())
                                .limit(limit))
        return list(reversed(result.all()))
    
    async def delete_chat_history(self, user_id: int) -> None:
        await self._db.execute(
            delete(ChatMessage).where(ChatMessage.user_id == user_id)
        )
        await self._db.commit()
