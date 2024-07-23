import os
import time

import psycopg2
from dotenv import load_dotenv
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

load_dotenv()

# Database connection parameters
DB_USER = os.getenv('POSTGRES_USER')
DB_PASSWORD = os.getenv('POSTGRES_PASSWORD')
DB_HOST = os.getenv('POSTGRES_HOST')
DB_PORT = os.getenv('POSTGRES_PORT')
DB_NAME = os.getenv('POSTGRES_DATABASE')


def connect_to_postgres():
    while True:
        try:
            conn = psycopg2.connect(
                dbname='postgres',
                user=DB_USER,
                password=DB_PASSWORD,
                host=DB_HOST,
                port=DB_PORT
            )
            return conn
        except psycopg2.OperationalError as e:
            print("PostgreSQL пока что не готов к использованию, повторная попытка через 5 секунд")
            time.sleep(5)


# Коннект к постгресу
conn = connect_to_postgres()
conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cur = conn.cursor()

# Тут чекаем есть ли такая база
cur.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{DB_NAME}';")
exists = cur.fetchone()

if not exists:
    cur.execute(f'CREATE DATABASE {DB_NAME};')

cur.close()
conn.close()

# Коннектимся к существующей, либо к только что созданной бд
conn = psycopg2.connect(
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT
)

# курсор
cur = conn.cursor()

# Сырой sql для создания баз
create_users_table = """
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    avatar VARCHAR(255)
);
"""

create_genres_table = """
CREATE TABLE IF NOT EXISTS genres (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);
"""

create_books_table = """
CREATE TABLE IF NOT EXISTS books (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    pages INTEGER NOT NULL,
    author_id INTEGER REFERENCES users(id),
    genres VARCHAR(255)
);
"""

create_booking_table = """
CREATE TABLE IF NOT EXISTS bookings (
    id SERIAL PRIMARY KEY,
    book_id INTEGER NOT NULL REFERENCES books(id),
    user_id INTEGER NOT NULL REFERENCES users(id),
    start_date TIMESTAMP NOT NULL,
    end_date TIMESTAMP NOT NULL,
    CONSTRAINT bookings_unique_booking UNIQUE (book_id, start_date, end_date)
);
"""

# Экзекутим в базу
cur.execute(create_users_table)
cur.execute(create_genres_table)
cur.execute(create_books_table)
cur.execute(create_booking_table)

# Комитим и закрываем коннект
conn.commit()
cur.close()
conn.close()

print("Таблицы успешно созданы")
