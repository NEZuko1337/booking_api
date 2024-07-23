import os

import psycopg2
from dotenv import load_dotenv

load_dotenv()

# Database connection parameters
DB_USER = os.getenv('POSTGRES_USER')
DB_PASSWORD = os.getenv('POSTGRES_PASSWORD')
DB_HOST = os.getenv('POSTGRES_HOST')
DB_PORT = os.getenv('POSTGRES_PORT')
DB_NAME = os.getenv('POSTGRES_DATABASE')

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT
)

# Create a cursor object
cur = conn.cursor()

# SQL commands to create tables
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
# Execute the SQL commands in the correct order
cur.execute(create_users_table)
cur.execute(create_genres_table)
cur.execute(create_books_table)
cur.execute(create_booking_table)

# Commit changes and close the connection
conn.commit()
cur.close()
conn.close()

print("Tables created successfully!")
