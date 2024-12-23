from pydantic import BaseModel

# Базовая схема пользователя
class UserBase(BaseModel):
    email: str

# Схема для создания пользователя
class UserCreate(UserBase):
    password: str

# Схема пользователя с дополнительными полями
class User(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True

# Базовая схема аудиофайла
class AudioFileBase(BaseModel):
    filename: str
    filepath: str

# Схема для создания аудиофайла
class AudioFileCreate(AudioFileBase):
    owner_id: int

# Схема аудиофайла с дополнительными полями
class AudioFile(AudioFileBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True

# Схема для ссылки на аудиофайл
class FileUrl(BaseModel):
    file_url: str

# Схема для токена
class Token(BaseModel):
    access_token: str
    token_type: str
