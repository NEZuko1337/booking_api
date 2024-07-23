# Booking API

Booking API - это RESTful API для управления бронированием книг. Проект написан на FastAPI с использованием SQLAlchemy для взаимодействия с базой данных и Celery + Redis для выполнения фоновых задач.

## Оглавление
- [Установка и запуск](#установка-и-запуск)
  - [Локальный запуск](#локальный-запуск)
  - [Запуск с Docker](#запуск-с-docker)
- [Использование](#использование)

## Установка и запуск

### Локальный запуск

1. Склонируйте репозиторий:

    ```bash
    git clone https://github.com/NEZuko1337/booking_api.git
    cd booking_api
    ```

2. Создайте и активируйте виртуальное окружение:

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # Для Windows используйте `venv\Scripts\activate`
    ```

3. Установите зависимости:

    ```bash
    pip install -r requirements.txt
    ```
   
4. Создайте файл `.env` в корне проекта и заполните его соответствующими значениями:

    ```plaintext
    POSTGRES_USER=YOUR_POSTGRES_USER
    POSTGRES_PASSWORD=YOUR_POSTGRES_PASS
    POSTGRES_HOST=db
    POSTGRES_PORT=YOUR_POSTGRES_PORT
    POSTGRES_DATABASE=YOUR_POSTRGES_DATABASE
    CELERY_BROKER_URL=YOUR_REDIS_BROKER_URL
    CELERY_RESULT_BACKEND=YOUR_REDIS_BACKEND_URL
    ```
   
5. Создайте базу данных и таблицы:

    ```bash
    python init_db.py
    ```
6. Запустите сервер:

    ```bash
    uvicorn app.main:app --reload
    ```

### Запуск с Docker

1. Склонируйте репозиторий:

    ```bash
    git clone https://github.com/NEZuko1337/booking_api.git
    cd booking_api
    ```

2. Создайте файл `.env` в корне проекта и заполните его соответствующими значениями:

    ```plaintext
    POSTGRES_USER=YOUR_POSTGRES_USER
    POSTGRES_PASSWORD=YOUR_POSTGRES_PASS
    POSTGRES_HOST=db
    POSTGRES_PORT=YOUR_POSTGRES_PORT
    POSTGRES_DATABASE=YOUR_POSTRGES_DATABASE
    CELERY_BROKER_URL=YOUR_REDIS_BROKER_URL
    CELERY_RESULT_BACKEND=YOUR_REDIS_BACKEND_URL
    ```

3. Запустите Docker Compose:

    ```bash
    docker-compose build --no-cache
    docker-compose up
    ```


## Использование

После запуска сервера API будет доступно по адресу `http://localhost:8000`.

Документация API доступна по адресу `http://localhost:8000/api/docs`.