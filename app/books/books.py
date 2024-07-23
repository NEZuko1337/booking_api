from typing import Optional, List

from fastapi import APIRouter, Query

from app.books.book import Book
from app.db.conntection import Transaction
from app.exceptions import NotFoundError
from app.protocol import Response
from app.schemas import BookView, BookViewModel

router = APIRouter()


@router.post("/")
async def add_book(book: BookView):
    async with Transaction():
        from app.users.user import User
        from app.genre.genre import Genre
        author = await User.get_author_by_id(book.author_id)
        genres_ids = [int(genre.id) for genre in await Genre.get_all_genres()]
        if author is not None and all(genre_id in genres_ids for genre_id in book.genres):
            book_id = await Book.create_book(
                title=book.title,
                price=book.price,
                pages=book.pages,
                author_id=book.author_id,
                genres=", ".join(map(str, book.genres))
            )
            return Response(
                message=f"Книга создана, ее id - {book_id}",
            )
    return NotFoundError(message="Автор книги не найден, или указаны не существующие жанры")


@router.put("/{id}")
async def update_book(book_id: int, data: BookView):
    async with Transaction():
        from app.users.user import User
        from app.genre.genre import Genre
        book = await Book.get_book_by_id(book_id=book_id)
        author = await User.get_author_by_id(data.author_id)
        genres_ids = [int(genre.id) for genre in await Genre.get_all_genres()]
        if book and author and all(genre_id in genres_ids for genre_id in data.genres):
            await Book.update_book(
                book_id=book_id,
                title=data.title,
                price=data.price,
                pages=data.pages,
                author_id=data.author_id,
                genres=", ".join(map(str, data.genres))
            )
            return Response(
                message="Книга изменена",
                payload=BookViewModel.from_orm(book)
            )
    return NotFoundError(message="Автор книги не найден, или указаны не существующие жанры")


@router.get("/filter")
async def filter_books(
        author_id: Optional[int] = Query(None),
        genre_ids: Optional[List[int]] = Query(None),
        min_price: Optional[float] = Query(None),
        max_price: Optional[float] = Query(None)
):
    async with Transaction():
        books = await Book.filter_books(
            author_id=author_id,
            genre_ids=genre_ids,
            min_price=min_price,
            max_price=max_price
        )
        if not books:
            return Response(message="Таких книжек не существует")
        return books


@router.get("/{id}")
async def get_book(book_id: int):
    async with Transaction():
        book = await Book.get_book_by_id(book_id=book_id)
        if book is not None:
            return Response(
                message="Книга существует",
                payload=BookViewModel.from_orm(book)
            )
    return NotFoundError(message="Книга не найдена")


@router.get("/")
async def get_books():
    async with Transaction():
        books = await Book.get_all_books()
        return books


@router.delete("/{id}")
async def delete_book(book_id: int):
    async with Transaction():
        book = await Book.get_book_by_id(book_id=book_id)
        if book is not None:
            await Book.delete_book(book_id=book_id)
            return Response(message=f"Книга с id {book_id} удалена успешно")
    return NotFoundError(message="Книга не найдена")
