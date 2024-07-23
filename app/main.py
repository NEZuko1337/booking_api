import uvicorn
from fastapi import FastAPI, Depends

from app.db import get_session
from app.routers import users, genres, books, bookings

# Инициализация приложения FastAPI
app = FastAPI(
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
    redoc_url=None,
    dependencies=[Depends(get_session)]
)

# Подключение роутеров
app.include_router(books.router, prefix="/books", tags=["Books"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(genres.router, prefix="/genres", tags=["Genres"])
app.include_router(bookings.router, prefix="/bookings", tags=["Bookings"])

# Основная точка входа
if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
