from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from sqlalchemy.future import select
from models.portfolio import User


# создание пользователя
async def create_user(session: AsyncSession,
                      username: str,
                      hashed_password: str,
                      email: str):
    try:
        new_user = User(username=username,
                        hashed_password=hashed_password,
                        email=email)
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        return new_user
    except IntegrityError:
        await session.rollback()
        raise HTTPException(status_code=400,
                            detail="Username or email already exists")


# возврат одного по id
async def get_user_by_id(session: AsyncSession, user_id: int):
    result = await session.execute(select(User).filter(User.id == user_id))
    return result.scalar_one_or_none()


# возврат по имени
async def get_user_by_username(session: AsyncSession, username: str):
    result = await session.execute(select(User).filter(User.username == username))
    return result.scalar_one_or_none()


# возврат всех
async def get_all_users(session: AsyncSession):
    result = await session.execute(select(User))
    return result.scalars().all()


# апдейт данных пользователя
async def update_user(session: AsyncSession,
                      user_id: int,
                      username: str,
                      hashed_password: str,
                      email: str):
    user = await get_user_by_id(session, user_id)
    if user:
        user.username = username
        user.hashed_password = hashed_password
        user.email = email
        await session.commit()
        await session.refresh(user)
    return user


# удаление пользователя
async def delete_user(session: AsyncSession, user_id: int):
    user = await get_user_by_id(session, user_id)
    if user:
        await session.delete(user)
        await session.commit()
    return user
