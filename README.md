# Auth API Server

Этот проект представляет собой сервер аутентификации, разработанный с использованием FastAPI. Сервер поддерживает асинхронные операции с использованием FastAPI, SQLAlchemy, JWT-аутентификацию, а также работу с базой данных PostgreSQL и кеширование через Redis.

## Основные технологии и зависимости:

- **FastAPI**: Основной фреймворк для создания API.
- **SQLAlchemy**: ORM для работы с базой данных.
- **Alembic**: Миграции базы данных.
- **asyncpg**: Асинхронный драйвер для PostgreSQL.
- **passlib**: Для хэширования паролей с использованием bcrypt.
- **JWT-аутентификация**: Реализована через библиотеку `async-fastapi-jwt-auth`.
- **httpx**: Асинхронный HTTP клиент для запросов к другим API.
- **Redis**: Используется для кеширования через `fastapi-cache2`.

## Установка проекта

1. Клонируйте репозиторий:

    ```bash
    git clone https://github.com/ваш-пользователь/ваш-репозиторий.git
    cd ваш-репозиторий
    ```

2. Создайте виртуальное окружение (рекомендуется):

    ```bash
    python -m venv venv
    ```

3. Активируйте виртуальное окружение:

   ```bash
    source venv/bin/activate  # для Linux/Mac
    .\venv\Scripts\activate  # для Windows
   ```

3. Установите зависимости:

    ```bash
    pip install -e .
    ```

4. Настройте базу данных PostgreSQL и примените миграции с помощью Alembic:

    ```bash
    alembic upgrade head
    ```

5. Запустите сервер:

    ```bash
    uvicorn main:app --reload
    ```

## Конфигурация

Проект использует переменные окружения для настройки подключения к базе данных, JWT и других параметров. Пример `.env` файла:

```env
DB_USER=DB_USER # Пользователь базы данных
DB_PASS=DB_PASS # Пароль пользователя базы данных
DB_HOST=DB_HOST # Хост на котором установлена база данных
DB_PORT=DB_PORT # Порт на котором установлена база данных
DB_NAME=DB_NAME # Имя базы данных

JWT_PRIVATE_KEY=JWT_PRIVATE_KEY # Приватный ключ для подписи JWT
JWT_PUBLIC_KEY=JWT_PUBLIC_KEY # Публичный ключ для проверки JWT

ACCESS_TOKEN_EXPIRES_IN=ACCESS_TOKEN_EXPIRES_IN # Время жизни токена доступа
REFRESH_TOKEN_EXPIRES_IN=REFRESH_TOKEN_EXPIRES_IN # Время жизни токена обновления
JWT_ALGORITHM=JWT_ALGORITHM # Алгоритм шифрования JWT
```

## Основные функции

- Регистрация и аутентификация пользователей.
- Управление пользователями (создание, удаление, редактирование).
- Защищенные маршруты с использованием JWT-аутентификации.
- Асинхронная работа с базой данных PostgreSQL.
- Кеширование данных с помощью Redis.


## Swagger

После установки и запуска проекта будет доступен [Swagger по адресу](http://localhost:8000/docs/)

для авторизации сразу же будут доступны два вида пользователя:

- User
    - email: `test_user@example.com`
    - password: `test`
- Admin
    - email: `test@example.com`
    - password: `test`