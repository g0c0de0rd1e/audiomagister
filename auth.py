from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession
import app.models as models
import app.schemas as schemas
import app.crud as crud
from app.database import get_db
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import create_async_engine
import os
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

# Конфигурация параметров аутентификации
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Настройка OAuth2 для аутентификации с использованием токена
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def create_access_token(data: dict, expires_delta: timedelta = None):
    """
    Создание токена доступа.
    :param data: данные для создания токена.
    :param expires_delta: время жизни токена.
    :return: созданный токен.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    """
    Получение текущего пользователя из токена.
    :param token: токен доступа.
    :param db: сессия базы данных.
    :return: текущий пользователь.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = await crud.get_user_by_email(db, email=email)
    if not user:
        raise credentials_exception
    return user
