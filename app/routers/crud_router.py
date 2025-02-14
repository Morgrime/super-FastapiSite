from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database.session import SessionLocal
from database.crud import (
    create_user, get_user_by_id, update_user,
    delete_user, get_all_users
)
from schemas.user_scheme import UserCreate, UserUpdate, User, UserDelete

router = APIRouter()


async def get_session():
    async with SessionLocal() as session:
        yield session


# создание пользователя
@router.post("/users/", response_model=UserCreate, tags=["CRUD"])
async def create_user_route(user: UserCreate,
                            session: AsyncSession = Depends(get_session)):
    hashed_password_str = str(user.hashed_password)
    try:
        new_user = await create_user(
            session,
            user.username,
            hashed_password_str,
            user.email)
        return new_user
    except HTTPException as e:
        raise e


# получение пользователя по id
@router.get("/users/{user_id}", response_model=UserCreate, tags=["CRUD"])
async def read_user_route(user_id: int,
                          session: AsyncSession = Depends(get_session)):
    user = await get_user_by_id(session, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# получение всех пользователей
@router.get("/users/", response_model=list[User], tags=["CRUD"])
async def get_users(session: AsyncSession = Depends(get_session)):
    users = await get_all_users(session)
    return users


# обновление пользователя по id
@router.put("/users/{user_id}", response_model=UserUpdate, tags=["CRUD"])
async def update_user_route(user_id: int,
                            user_update: UserUpdate,
                            session: AsyncSession = Depends(get_session)):
    user = await update_user(session,
                             user_id,
                             user_update.username,
                             user_update.hashed_password,
                             user_update.email)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# удаление пользователя по id
@router.delete("/users/{user_id}", response_model=UserDelete, tags=["CRUD"])
async def delete_user_route(user_id: int,
                            session: AsyncSession = Depends(get_session)):
    user = await delete_user(session, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {"detail": "User deleted successfully"}
