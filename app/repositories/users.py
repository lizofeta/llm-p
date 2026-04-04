# Доступ к таблице users

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import User
from app.schemas.user import UserPublic
from app.core.enums import Role

class UserStorage:
    def __init__(self, db: AsyncSession):
        self._db = db 
    
    def _to_response(self, user: User) -> UserPublic:
        return UserPublic.model_validate()
    
    async def get_user_by_id(self, user_id: int) -> UserPublic | None:
        user = await self._db.get(User, user_id)
        if user is None:
            return None 
        return self._to_response(user)
    
    async def get_user_by_email(self, user_email: str) -> UserPublic | None:
        query = select(User).where(User.email == user_email)
        result = await self._db.execute(query)
        user = result.scalar_one_or_none()
        if user is None:
            return None 
        return self._to_response(user)
    
    async def create_user(
            self,
            email: str,
            password_hash: str,
            role: Role = Role.USER
            ) -> UserPublic:
        user = User(
            email=email,
            password_hash=password_hash,
            role=role
        )
        self._db.add(user)
        await self._db.commit()
        await self._db.refresh(user)
        return self._to_response(user)
