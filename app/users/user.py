import sqlalchemy as sa

from app.db.base import Base
from app.db.conntection import db_session


class User(Base):
    __tablename__ = 'users'

    id = sa.Column(sa.Integer, primary_key=True, index=True)
    first_name = sa.Column(sa.String, index=True)
    last_name = sa.Column(sa.String, index=True)
    avatar = sa.Column(sa.String, index=True)

    @classmethod
    async def create_user(cls, first_name: str, last_name: str, avatar: str):
        query = (
            sa.insert(User)
        ).values(
            first_name=first_name,
            last_name=last_name,
            avatar=avatar,
        ).returning(User.id)
        created_author = await db_session.get().execute(query)
        return created_author.scalars().first()

    @classmethod
    async def update_user(cls, user_id: int, first_name: str, last_name: str):
        query = (
            sa.update(User).where(User.id == user_id)
        ).values(
            first_name=first_name,
            last_name=last_name,
        ).returning(User)
        updated_author = await db_session.get().execute(query)
        return updated_author.scalars().first()

    @classmethod
    async def get_author_by_id(cls, user_id: id):
        query = sa.select(User).where(User.id == user_id)
        author = await db_session.get().execute(query)
        return author.scalars().first()

    @classmethod
    async def get_all_authors(cls):
        query = sa.select(User)
        authors = await db_session.get().execute(query)
        return authors.scalars().all()

    @classmethod
    async def delete_user(cls, user_id: int):
        query = (
            sa.delete(cls).where(cls.id == user_id)
        )
        await db_session.get().execute(query)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.id}"
