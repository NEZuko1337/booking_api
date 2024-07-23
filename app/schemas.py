from datetime import date

from pydantic import BaseModel


class UserRegistrationView(BaseModel):
    first_name: str
    last_name: str
    avatar: str


class UserUpdateView(BaseModel):
    first_name: str
    last_name: str


class UserView(BaseModel):
    first_name: str
    last_name: str
    avatar: str

    class Config:
        orm_mode = True


class GenreView(BaseModel):
    name: str

    class Config:
        orm_mode = True


class BookView(BaseModel):
    title: str
    price: float
    pages: int
    author_id: int
    genres: list[int]

    class Config:
        orm_mode = True


class BookViewModel(BaseModel):
    title: str
    price: float
    pages: int
    author_id: int
    genres: str

    class Config:
        orm_mode = True


class BookingView(BaseModel):
    book_id: int
    user_id: int
    start_date: date
    end_date: date

    class Config:
        orm_mode = True
