from fastapi import APIRouter, HTTPException

from app.bookings.booking import Booking
from app.db.conntection import Transaction
from app.protocol import Response
from app.schemas import BookingView

router = APIRouter()


@router.post("/")
async def create_booking(data: BookingView):
    async with Transaction():
        from app.users.user import User
        from app.books.book import Book
        is_available = await Book.is_available(book_id=data.book_id, start_date=data.start_date, end_date=data.end_date)
        author = await User.get_author_by_id(data.user_id)
        print(is_available, author)
        if not author:
            return Response(code=404, message="Автор книги не найден!")
        if not is_available:
            return Response(code=401, message="На выбранные даты, книга не доступна, пожалуйста выберите другую дату")
        booking_id = await Booking.create_booking(book_id=data.book_id, user_id=data.user_id,
                                                  start_date=data.start_date, end_date=data.end_date)
        return Response(message="Бронь успешно создана", payload={"booking_id": booking_id})


@router.delete("/{id}")
async def delete_booking(booking_id: int):
    async with Transaction():
        booking = await Booking.get_booking_by_id(booking_id=booking_id)
        if not booking:
            raise HTTPException(status_code=404, detail="Бронь не найдена")

        await Booking.delete_booking(booking_id=booking_id)
        return Response(message="Бронь удалена")
