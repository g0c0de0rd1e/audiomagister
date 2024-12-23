# API Документация

## Базовый URL
`http://your-server.com/api`

## Параметры авторизации
Используется авторизация по токенам (Bearer Token).

## Маршруты

### 1. Получение токена
**POST** `/token`

Получение токена для аутентификации.

**Параметры:**
- `username` (str): Email пользователя.
- `password` (str): Пароль пользователя.

**Пример запроса:**
```json
{
    "username": "user@example.com",
    "password": "password"
}
```

**Ответ**
```json
{
    "access_token": "токен_доступа",
    "token_type": "bearer"
}
```

### 2. Регистрация пользователя
**POST** `/register/`

Регистрация нового пользователя.

**Параметры:**
- `email` (str): Email пользователя.
- `password` (str): Пароль пользователя.

**Пример запроса:**
```json
{
    "email": "newuser@example.com",
    "password": "newpassword"
}
``` 
**Ответ**
```json
{
    "id": 1,
    "email": "newuser@example.com",
    "is_active": true
}
```

### 3. Авторизация пользователя
**POST** `/login/`

Авторизация пользователя.

**Параметры:**
- `email` (str): Email пользователя.
- `password` (str): Пароль пользователя.

**Пример запроса:**
```json
{
    "email": "user@example.com",
    "password": "password"
}
```

**Ответ**
```json
{
    "message": "Login successful"
}
```

### 4. Загрузка аудиофайла
**POST** `/uploadfile/`

Загрузка аудиофайлов на сервер.

**Параметры:**
- `file` (UploadFile): Загружаемый аудиофайл.

**Пример запроса:**
```shell
curl -X 'POST' \
  'http://your-server.com/api/uploadfile/' \
  -H 'Authorization: Bearer токен_доступа' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@path/to/your/audiofile.mp3'
```

**Ответ**
```json
{
    "id": 1,
    "filename": "audiofile.mp3",
    "filepath": "uploads/audiofile.mp3",
    "owner_id": 1
}
```

### 5. Получение аудиофайла
**GET** `/files/{file_name}`

Получение аудиофайла по имени.

**Параметры:**
- `file_name` (str): Имя файла.

**Пример запроса:**
```shell
curl -X 'GET' \
  'http://your-server.com/api/files/audiofile.mp3' \
  -H 'accept: application/json'
```

**Ответ**
```json
{
    "file_url": "http://your-server.com/uploads/audiofile.mp3"
}
```