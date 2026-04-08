# В этом модуле реализована вся криптография и безопасность

from datetime import datetime, timedelta, timezone

from jose import jwt, ExpiredSignatureError, JWTError
from passlib.context import CryptContext
from app.core.errors import UnauthorizedError

# создаем менеджер хеширования паролей 
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# функция хеширования 
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# функция проверки пароля
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# функция создания access token
def create_access_token(
        data: dict, 
        expire_minutes: int, 
        secret: str,
        algorithm: str
        ) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        **data,
        "exp": now + timedelta(minutes=expire_minutes),
        "iat": now
    }
    return jwt.encode(
        payload, 
        secret, 
        algorithm=algorithm)

# функция декодирования access token 
def decode_access_token(
        token: str,
        secret: str,
        algorithm: str
        ) -> dict:
    try:
        return jwt.decode(
            token,
            secret,
            algorithms=[algorithm]
        )
    except ExpiredSignatureError as e:
        raise UnauthorizedError("Токен истёк") from e 
    except JWTError as e:
        raise UnauthorizedError("Некорректный токен") from e
    