from fastapi import APIRouter

from app.db.conntection import Transaction
from app.exceptions import NotFoundError
from app.models import Genre
from app.protocol import Response
from app.schemas import GenreView

router = APIRouter()


@router.get("/{id}")
async def get_genre(genre_id: int):
    async with Transaction():
        genre = await Genre.get_genre_by_id(genre_id=genre_id)
        if genre is not None:
            return Response(
                message="Жанр книги существует",
                payload=GenreView.from_orm(genre)
            )
    return NotFoundError


@router.get("/")
async def get_genres():
    async with Transaction():
        genres = await Genre.get_all_genres()
        return genres


@router.post("/")
async def create_genre(data: GenreView):
    async with Transaction():
        genre_id = await Genre.create_genre(
            genre_name=data.name
        )
    return Response(
        message=f"Жанр книги создан, его id {genre_id}",
    )


@router.put("/{id}")
async def update_genre(genre_id: int, data: GenreView):
    async with Transaction():
        genre = await Genre.get_genre_by_id(genre_id=genre_id)
        if genre is not None:
            updated_genre = await Genre.update_genre(genre_id=genre_id, genre_name=data.name)
            return Response(
                message="Жанр изменен",
                payload=GenreView.from_orm(updated_genre)
            )
    return NotFoundError


@router.delete("/{id}")
async def delete_genre(genre_id: int):
    async with Transaction():
        genre = await Genre.get_genre_by_id(genre_id=genre_id)
        if genre is not None:
            await Genre.delete_genre(genre_id=genre_id)
            return Response(message="Жанр удален")
    return NotFoundError
