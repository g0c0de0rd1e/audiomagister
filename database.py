from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

# Строка подключения к базе данных
DATABASE_URL = os.getenv("DATABASE_URL")

# Создание асинхронного двигателя для подключения к базе данных
engine = create_async_engine(DATABASE_URL)
# Создание сессии для взаимодействия с базой данных
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

# Создание базового класса для моделей
Base = declarative_base()

def get_db():
    """
    Получение сессии базы данных.
    :return: генератор сессии базы данных.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
