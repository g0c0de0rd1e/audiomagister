from fastapi import FastAPI, Depends, HTTPException, File, UploadFile, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import FileResponse
from app.database import SessionLocal, get_db
import app.crud as crud
import app.models as models
import app.schemas as schemas
import app.auth as auth
from datetime import timedelta
from app.auth import get_current_user, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES

# Инициализация приложения FastAPI
app = FastAPI()

# Настройка CORS для взаимодействия с фронтендом
origins = [
    "http://localhost:3000",  # Для локальной разработки
    "https://your-react-app-domain.com"  # Для продакшн-домена
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Разрешенные источники
    allow_credentials=True,  # Разрешенные учетные данные
    allow_methods=["*"],  # Разрешенные методы (GET, POST и т.д.)
    allow_headers=["*"],  # Разрешенные заголовки
)

# Создание таблиц в базе данных
models.Base.metadata.create_all(bind=auth.engine)

@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    """
    Получение токена для аутентификации.
    :param form_data: данные формы с полями "username" и "password".
    :param db: сессия базы данных.
    :return: токен доступа.
    """
    user = await crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/uploadfile/", response_model=schemas.AudioFile)
async def upload_file(file: UploadFile, db: AsyncSession = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    """
    Загрузка аудиофайлов на сервер.
    :param file: загружаемый файл.
    :param db: сессия базы данных.
    :param current_user: текущий аутентифицированный пользователь.
    :return: информация о загруженном аудиофайле.
    """
    file_location = f"uploads/{file.filename}"
    # Сохраняем файл на сервере
    with open(file_location, "wb+") as file_object:
        file_object.write(file.file.read())
    
    # Создаем запись о файле в базе данных
    audio_file = schemas.AudioFileCreate(
        filename=file.filename, 
        filepath=file_location, 
        owner_id=current_user.id
    )
    return await crud.create_audio_file(db=db, audio_file=audio_file)

@app.get("/files/{file_name}", response_model=schemas.FileUrl)
async def get_file(file_name: str):
    """
    Получение URL аудиофайла по имени.
    :param file_name: имя файла.
    :return: URL файла.
    """
    file_location = f"uploads/{file_name}"
    file_url = f"http://your-server.com/{file_location}"
    return {"file_url": file_url}

@app.post("/register/", response_model=schemas.User)
async def register_user(user: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    """
    Регистрация нового пользователя.
    :param user: данные нового пользователя.
    :param db: сессия базы данных.
    :return: информация о зарегистрированном пользователе.
    """
    db_user = await crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return await crud.create_user(db=db, user=user)

@app.post("/login/")
async def login(user: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    """
    Авторизация пользователя.
    :param user: данные пользователя.
    :param db: сессия базы данных.
    :return: сообщение об успешной авторизации.
    """
    db_user = await crud.get_user_by_email(db, email=user.email)
    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    return {"message": "Login successful"}
