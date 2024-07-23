from datetime import date
from typing import Optional, List

import sqlalchemy as sa
from sqlalchemy import Column, Integer, String, ForeignKey, DECIMAL

from app.db import Base
from app.db.conntection import db_session


class Book(Base):
    from app.users.user import User
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    price = Column(DECIMAL(10, 2))
    pages = Column(Integer)
    author_id = Column(Integer, ForeignKey('users.id'))
    genres = Column(String, index=True)

    @classmethod
    async def create_book(cls, title: str, price: float, pages: int, author_id: int, genres: str):
        query = (
            sa.insert(Book)
        ).values(
            title=title,
            price=price,
            pages=pages,
            author_id=author_id,
            genres=genres
        ).returning(Book.id)
        created_book = await db_session.get().execute(query)
        return created_book.scalars().first()

    @classmethod
    async def get_book_by_id(cls, book_id: int):
        query = sa.select(Book).where(Book.id == book_id)
        book = await db_session.get().execute(query)
        return book.scalars().first()

    @classmethod
    async def get_all_books(cls):
        query = sa.select(Book)
        books = await db_session.get().execute(query)
        return books.scalars().all()

    @classmethod
    async def update_book(cls, book_id: int, title: str, price: float, pages: int, author_id: int, genres: str):
        query = (
            sa.update(Book).where(Book.id == book_id)
        ).values(
            title=title,
            price=price,
            pages=pages,
            author_id=author_id,
            genres=genres
        ).returning(Book)
        updated_book = await db_session.get().execute(query)
        return updated_book.scalars().first()

    @classmethod
    async def delete_book(cls, book_id: int):
        query = (
            sa.delete(cls).where(cls.id == book_id)
        )
        await db_session.get().execute(query)

    @classmethod
    async def filter_books(cls, author_id: Optional[int] = None,
                           genre_ids: Optional[List[int]] = None,
                           min_price: Optional[float] = None,
                           max_price: Optional[float] = None):
        query = sa.select(Book)

        if author_id:
            query = query.where(Book.author_id == author_id)

        if genre_ids:
            genre_conditions = [Book.genres.contains(f'{genre_id}') for genre_id in genre_ids]
            query = query.where(sa.or_(*genre_conditions))

        if min_price is not None:
            query = query.where(Book.price >= min_price)

        if max_price is not None:
            query = query.where(Book.price <= max_price)

        books = await db_session.get().execute(query)
        return books.scalars().all()

    @classmethod
    async def is_available(cls, book_id: int, start_date: date, end_date: date):
        from app.bookings.booking import Booking
        query = sa.select(Booking).where(
            sa.and_(
                Booking.book_id == book_id,
                sa.or_(
                    sa.and_(
                        Booking.start_date >= start_date,
                        Booking.end_date <= end_date
                    ),
                    sa.and_(
                        Booking.start_date <= start_date,
                        Booking.end_date > end_date
                    )
                )
            )
        )
        existing_bookings = await db_session.get().execute(query)
        return not existing_bookings.scalars().first()
