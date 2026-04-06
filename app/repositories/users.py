# Доступ к таблице users

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import User
from app.core.enums import Role

class UserStorage:
    def __init__(self, db: AsyncSession):
        self._db = db 
    
    async def get_user_by_id(self, user_id: int) -> User | None:
        user = await self._db.get(User, user_id)
        if user is None:
            return None 
        return user
    
    async def get_user_by_email(self, user_email: str) -> User | None:
        query = select(User).where(User.email == user_email)
        result = await self._db.execute(query)
        user = result.scalar_one_or_none()
        if user is None:
            return None 
        return user
    
    async def create_user(
            self,
            email: str,
            password_hash: str,
            role: Role = Role.USER
            ) -> User:
        user = User(
            email=email,
            password_hash=password_hash,
            role=role
        )
        self._db.add(user)
        await self._db.commit()
        await self._db.refresh(user)
        return user
