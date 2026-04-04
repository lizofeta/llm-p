# Доступ к таблице чатов

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete

from app.schemas.chat import ChatResponse
from app.db.models import ChatMessage, User

class ChatMessagesStorage:
    def __init__(self, db: AsyncSession):
        self._db = db 
    
    def _to_response(self, chat_message: ChatMessage) -> ChatResponse:
        return ChatResponse(
            answer=chat_message.content
        )
    
    async def add_message(
            self, 
            user: User, 
            message_data: dict[str, str]
            ) -> ChatResponse:
        message = ChatMessage(
            user_id=user.id,
            role=message_data["role"],
            content=message_data["content"]
        )
        self._db.add(message)
        await self._db.commit()
        await self._db.refresh(message)
        return self._to_response(message)
    
    async def show_last_n_messages(
            self, 
            user: User, 
            limit: int
            ) -> list[ChatResponse]:
        result = await self._db.scalars(select(ChatMessage)
                                .where(ChatMessage.user_id == user.id)
                                .order_by(ChatMessage.id.desc())
                                .limit(limit))
        messages = result.all()
        messages.reverse()
        return [self._to_response(message) for message in messages]
    
    async def delete_chat_history(self, user: User) -> None:
        await self._db.execute(
            delete(ChatMessage).where(ChatMessage.user_id == user.id)
        )
        await self._db.commit()
