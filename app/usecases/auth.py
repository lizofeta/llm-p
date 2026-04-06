# Бизнес логика регистрации и авторизации

from app.repositories.users import UserStorage
from app.db.models import User
from app.core.config import Settings
from app.core.errors import EmailAlreadyExistsError, NotFoundError, UnauthorizedError
from app.core.security import hash_password, verify_password, create_access_token, decode_access_token


class AuthUseCase:
    def __init__(
            self, 
            users_repository: UserStorage,
            settings: Settings) -> None:
        self._users_repository = users_repository
        self._settings = settings
    
    async def register(self, email: str, password: str) -> User:
        # Проверка, что email не занят 
        existing_user = await self._users_repository.get_user_by_email(email)
        if existing_user is not None:
            raise EmailAlreadyExistsError()

        hashed_pwd = hash_password(password)
        user = (await self._users_repository
                        .create_user(
                            email=email, 
                            password_hash=hashed_pwd
                            ))
        return user
    
    async def login(self, email: str, password: str) -> str:
        user = await self._users_repository.get_user_by_email(email)
        if user is None:
            raise UnauthorizedError(
                f"Неверный email или пароль"
                )
        
        if not verify_password(
            plain_password=password, 
            hashed_password=user.password_hash):
            raise UnauthorizedError(
                "Неверный email или пароль"
                )
        
        access_token = create_access_token(
            data={"sub": str(user.id),
                  "role": user.role},
            expire_minutes=self._settings.access_token_expire_minutes,
            secret=self._settings.jwt_secret,
            algorithm=self._settings.jwt_alg
        )

        return access_token
    
    async def get_user_by_id(self, user_id: int) -> User:
        user = await self._users_repository.get_user_by_id(user_id)
        if user is None:
            raise NotFoundError("Пользователь не найден")
        return user
    
    async def get_current_user(self, token: str) -> User:
        try:
            payload = decode_access_token(
                token=token,
                secret=self._settings.jwt_secret,
                algorithm=self._settings.jwt_alg
                )
        except ValueError as e:
            raise UnauthorizedError() from e 
        
        user_id = payload.get("sub")
        token_role = payload.get("role")
        if not user_id or not token_role:
            raise UnauthorizedError("Некорректный payload токена")
        
        db_user = await self.get_user_by_id(int(user_id))
        
        if db_user.role != token_role:
            raise UnauthorizedError("Роль в токене не совпадает с ролью в БД")
        
        return db_user
