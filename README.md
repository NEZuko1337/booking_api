﻿# Booking API

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
6. (Опционально) Можно создать базу вручную, но перед этим не забудьте внести ее название в .env, ниже будет сырой sql код для создания баз. Создавать именно в таком порядке, после 4х баз будут еще входные данные, которые при желании можно вставить также сырым sql, либо реализовать свои в CRUD
   ```sql
    CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    avatar VARCHAR(255)
   );
   CREATE TABLE IF NOT EXISTS genres (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL
   );
   CREATE TABLE IF NOT EXISTS books (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    pages INTEGER NOT NULL,
    author_id INTEGER REFERENCES users(id),
    genres VARCHAR(255)
   );
   CREATE TABLE IF NOT EXISTS bookings (
    id SERIAL PRIMARY KEY,
    book_id INTEGER NOT NULL REFERENCES books(id),
    user_id INTEGER NOT NULL REFERENCES users(id),
    start_date TIMESTAMP NOT NULL,
    end_date TIMESTAMP NOT NULL,
    CONSTRAINT bookings_unique_booking UNIQUE (book_id, start_date, end_date)
   );
   
   -- Вставка пользователей(Данные для бд)
   INSERT INTO users (first_name, last_name, avatar) VALUES
   ('John', 'Doe', 'avatar1.jpg'),
   ('Jane', 'Smith', 'avatar2.jpg'),
   ('Alice', 'Johnson', 'avatar3.jpg');
   
   -- Вставка жанров
   INSERT INTO genres (name) VALUES
   ('Science Fiction'),
   ('Fantasy'),
   ('Non-Fiction');
   
   -- Вставка книг
   INSERT INTO books (title, price, pages, author_id, genres) VALUES
   ('The Future of Us', 19.99, 350, 1, '1,2'),
   ('The Magic Forest', 15.50, 280, 2, '2'),
   ('The Real World', 22.00, 400, 3, '3');
   
   -- Вставка бронирований
   INSERT INTO bookings (book_id, user_id, start_date, end_date) VALUES
   (1, 2, '2024-07-01 00:00:00', '2024-07-10 00:00:00'),
   (2, 1, '2024-07-05 00:00:00', '2024-07-15 00:00:00'),
   (3, 2, '2024-07-11 00:00:00', '2024-07-18 00:00:00');

    ```
7. Запустите сервер:

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
