from datetime import date

import sqlalchemy as sa
from sqlalchemy import Column, Integer, ForeignKey, Date

from app.db import Base
from app.db.conntection import db_session


class Booking(Base):
    __tablename__ = 'bookings'

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey('books.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)

    @classmethod
    async def create_booking(cls, book_id: int, user_id: int, start_date: date, end_date: date):
        query = sa.insert(Booking).values(
            book_id=book_id,
            user_id=user_id,
            start_date=start_date,
            end_date=end_date
        ).returning(Booking.id)
        created_book = await db_session.get().execute(query)
        return created_book.scalars().first()

    @classmethod
    async def get_booking_by_id(cls, booking_id: int):
        query = sa.select(Booking).where(Booking.id == booking_id)
        booking = await db_session.get().execute(query)
        return booking.scalars().first()

    @classmethod
    async def get_bookings_by_book_id(cls, book_id: int):
        query = sa.select(Booking).where(Booking.book_id == book_id)
        bookings = await db_session.get().execute(query)
        return bookings.scalars().all()

    @classmethod
    async def delete_booking(cls, booking_id: int):
        query = (
            sa.delete(cls).where(cls.id == booking_id)
        )
        await db_session.get().execute(query)
