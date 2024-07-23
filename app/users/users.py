from fastapi import APIRouter

from app.db.conntection import Transaction
from app.exceptions import NotFoundError

from app.protocol import Response
from app.schemas import UserRegistrationView, UserView, UserUpdateView
from app.users.user import User

router = APIRouter()


@router.get("/{id}")
async def get_user(user_id: int):
    async with Transaction():
        user = await User.get_author_by_id(user_id=user_id)
        if user is not None:
            return Response(
                message="Автор существует",
                payload=UserView.from_orm(user)
            )
    return NotFoundError


@router.get("/")
async def get_users():
    async with Transaction():
        users = await User.get_all_authors()
        return users


@router.post("/")
async def create_user(data: UserRegistrationView):
    async with Transaction():
        user_id = await User.create_user(
            first_name=data.first_name,
            last_name=data.last_name,
            avatar=data.avatar
        )
    return Response(
        message=f"Автор создан, его id {user_id}",
    )


@router.put("/{id}")
async def update_user(user_id: int, data: UserUpdateView):
    async with Transaction():
        user = await User.get_author_by_id(user_id=user_id)
        if user is not None:
            updated_user = await User.update_user(user_id=user_id, first_name=data.first_name, last_name=data.last_name)
            return Response(
                message="Автор изменен",
                payload=UserView.from_orm(updated_user)
            )
    return NotFoundError


@router.delete("/{id}")
async def delete_user(user_id: int):
    async with Transaction():
        user = await User.get_author_by_id(user_id=user_id)
        if user is not None:
            await User.delete_user(user_id=user_id)
            return Response(message="Автор удален")
    return NotFoundError
