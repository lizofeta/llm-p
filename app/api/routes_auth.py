# HTTP-ендпоинты авторизации 

from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from typing import Annotated

from app.api.deps import AuthUseCaseDep, UserIDDEP
from app.schemas.auth import TokenResponse, RegisterRequest
from app.schemas.user import UserPublic

from app.core.errors import EmailAlreadyExistsError, UnauthorizedError, NotFoundError

OAuth2RequestFormDep = Annotated[OAuth2PasswordRequestForm, Depends()]

auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.post(
    "/register",
    response_model=UserPublic,
    status_code=status.HTTP_201_CREATED
)
async def register(
    data: RegisterRequest,
    auth_usecase: AuthUseCaseDep
) -> UserPublic:
    try:
        user = await auth_usecase.register(data.email, data.password)
        return user
    except EmailAlreadyExistsError as e:
        raise HTTPException(
            status_code=409,
            detail=str(e)
        )

@auth_router.post(
    "/login",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK
)
async def login(
    data: OAuth2RequestFormDep,
    auth_usecase: AuthUseCaseDep
) -> TokenResponse:
    try:
        token = await auth_usecase.login(
            email=data.username, 
            password=data.password
        )
        return TokenResponse(access_token=token)
    except UnauthorizedError as e:
        raise HTTPException(
            status_code=401,
            detail=str(e)
        )

@auth_router.get(
    "/me",
    response_model=UserPublic,
    status_code=status.HTTP_200_OK
)
async def me(
    user_id: UserIDDEP,
    auth_usecase: AuthUseCaseDep
) -> UserPublic:
    try:
        user = await auth_usecase.get_user_by_id(user_id)
        return user
    except NotFoundError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )
