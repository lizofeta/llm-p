# Dependency Injection (фабрика зависимостей)

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings, Settings
from app.core.security import decode_access_token
from app.db.session import get_db
from app.usecases.auth import AuthUseCase
from app.usecases.chat import ChatUseCase
from app.repositories.users import UserStorage
from app.repositories.chat_messages import ChatMessagesStorage
from app.services.openrouter_client import OpenRouterClient

from app.core.errors import UnauthorizedError


SettingsDep = Annotated[Settings, Depends(get_settings)]
DBDep = Annotated[AsyncSession, Depends(get_db)]

def get_users_storage(db: DBDep) -> UserStorage:
    return UserStorage(db)

def get_chats_storage(db: DBDep) -> ChatMessagesStorage:
    return ChatMessagesStorage(db)

def get_or_client(settings: SettingsDep) -> OpenRouterClient:
    return OpenRouterClient(settings)


# usecases

def get_auth_usecase(
        users_repo: Annotated[UserStorage, Depends(get_users_storage)],
        settings: SettingsDep
) -> AuthUseCase:
    return AuthUseCase(users_repo, settings)

AuthUseCaseDep = Annotated[AuthUseCase, Depends(get_auth_usecase)]

def get_chat_usecase(
        chats_repo: Annotated[ChatMessagesStorage, Depends(get_chats_storage)],
        or_client: Annotated[OpenRouterClient, Depends(get_or_client)],
        settings: SettingsDep
) -> ChatUseCase:
    return ChatUseCase(
        chat_repository=chats_repo,
        or_client=or_client,
        settings=settings
    )

ChatUseCaseDep = Annotated[ChatUseCase, Depends(get_chat_usecase)]


# OAuth2

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user_id(
        token: Annotated[str, Depends(oauth2_scheme)],
        settings: SettingsDep
) -> int:
    try:
        payload = decode_access_token(
            token=token,
            secret=settings.jwt_secret,
            algorithm=settings.jwt_alg
        )

        user_id = payload.get("sub")
        
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Некорректные данные аутентификации"
            )
        
        try:
            return int(user_id)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Некорректный формат user_id"
            )

    except UnauthorizedError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )
    
UserIDDEP = Annotated[int, Depends(get_current_user_id)]
