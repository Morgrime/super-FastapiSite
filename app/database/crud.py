from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.portfolio import User
from app.database.session import SessionLocal

async def create_user(session: AsyncSession, 
                      username: str,
                      hashed_password: str,
                      email: str):
    new_user = User(username, hashed_password, email)
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return new_user


async def get_user(session: AsyncSession, user_id: int):
    result = await session.execute(select(User).filter(User.id==user_id))
    return result.scalar_one_or_none


async def update_user(session: AsyncSession, 
                      user_id: int,
                      username: str,
                      hashed_password: str,
                      email: str):
    user = await get_user(session, user_id)
    if user:
        user.username = username
        user.hashed_password = hashed_password
        user.email = email
        await session.commit()
        await session.refresh(user)
    return user


async def delete_user(session: AsyncSession, user_id: int):
    user = await get_user(session, user_id)
    if user:
        await session.delete(user)
        await session.commit()
    return user