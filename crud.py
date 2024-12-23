from sqlalchemy.ext.asyncio import AsyncSession
import app.models as models
import app.schemas as schemas
from passlib.context import CryptContext

# Настройка хэширования паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def get_user_by_email(db: AsyncSession, email: str):
    """
    Получение пользователя по email.
    :param db: сессия базы данных.
    :param email: email пользователя.
    :return: пользователь или None.
    """
    result = await db.execute(
        models.User.select().where(models.User.email == email)
    )
    return result.scalar_one_or_none()

async def create_user(db: AsyncSession, user: schemas.UserCreate):
    """
    Создание нового пользователя.
    :param db: сессия базы данных.
    :param user: данные нового пользователя.
    :return: созданный пользователь.
    """
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def authenticate_user(db: AsyncSession, email: str, password: str):
    """
    Аутентификация пользователя.
    :param db: сессия базы данных.
    :param email: email пользователя.
    :param password: пароль пользователя.
    :return: пользователь или False.
    """
    user = await get_user_by_email(db, email=email)
    if not user or not pwd_context.verify(password, user.hashed_password):
        return False
    return user

async def create_audio_file(db: AsyncSession, audio_file: schemas.AudioFileCreate):
    """
    Создание новой записи аудиофайла.
    :param db: сессия базы данных.
    :param audio_file: данные аудиофайла.
    :return: созданная запись аудиофайла.
    """
    db_audio_file = models.AudioFile(**audio_file.dict())
    db.add(db_audio_file)
    await db.commit()
    await db.refresh(db_audio_file)
    return db_audio_file
