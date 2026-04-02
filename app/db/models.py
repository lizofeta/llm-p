# ORM модели
from app.db.base import Base
from app.core.enums import Role, MessageRole

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, Integer, Enum, DateTime, ForeignKey, func

from datetime import datetime

# model User
class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String, nullable=False) 
    role: Mapped[Role] = mapped_column(
        Enum(
            Role,
            values_callable=lambda values: [item.value for item in values],
            native_enum=False
        ),
        nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now(),
        nullable=False
        )
    
    # relationship с таблицей chat_messages
    chat_messages: Mapped[list["ChatMessage"]] = relationship(back_populates="user")


# model ChatMessage
class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    role: Mapped[MessageRole] = mapped_column(
        Enum(
            MessageRole,
            values_callable=lambda values: [item.value for item in values],
            native_enum=False
        ),
        nullable=False
    )
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now(),
        nullable=False
        )
    
    # relationship с таблицей users
    user: Mapped["User"] = relationship(back_populates="chat_messages")
