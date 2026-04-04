# Pydantic схема для пользователя

from pydantic import BaseModel, EmailStr

from app.core.enums import Role

class UserPublic(BaseModel):
    id: int 
    email: EmailStr
    role: Role 
    model_config = {"from_attributes": True}
