import sqlalchemy as sa
from sqlalchemy import Column, Integer, String

from app.db import Base
from app.db.conntection import db_session


class Genre(Base):
    __tablename__ = 'genres'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

    @classmethod
    async def create_genre(cls, genre_name: str):
        query = (
            sa.insert(Genre)
        ).values(
            name=genre_name
        ).returning(Genre.id)
        created_genre = await db_session.get().execute(query)
        return created_genre.scalars().first()

    @classmethod
    async def update_genre(cls, genre_id: int, genre_name: str):
        query = (
            sa.update(Genre).where(Genre.id == genre_id)
        ).values(
            name=genre_name
        ).returning(Genre)
        updated_genre = await db_session.get().execute(query)
        return updated_genre.scalars().first()

    @classmethod
    async def get_genre_by_id(cls, genre_id: id):
        query = sa.select(Genre).where(Genre.id == genre_id)
        genre = await db_session.get().execute(query)
        return genre.scalars().first()

    @classmethod
    async def get_all_genres(cls):
        query = sa.select(Genre)
        genres = await db_session.get().execute(query)
        return genres.scalars().all()

    @classmethod
    async def delete_genre(cls, genre_id: int):
        query = (
            sa.delete(cls).where(cls.id == genre_id)
        )
        await db_session.get().execute(query)
