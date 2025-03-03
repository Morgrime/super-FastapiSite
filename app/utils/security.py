from passlib.context import CryptContext
from database.crud import get_user_by_username
from sqlalchemy.ext.asyncio import AsyncSession

pwd_context = CryptContext(schemes=["bcrypt"])


# хэш пароля
def hash_password(password: str) -> str:
    return pwd_context.hash(password)


# проверка пароля
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# смена пароля auth_router.py /change_password
async def change_password(session: AsyncSession,
                          user_data: dict,
                          old_password: str,
                          new_password: str) -> bool:
    username = user_data.get("sub")
    if not username:
        raise ValueError("Invalid token data")

    db_user = await get_user_by_username(session, username)
    if not verify_password(old_password, db_user.hashed_password):
        raise ValueError("Invalid old password")

    db_user.hashed_password = hash_password(new_password)
    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)
    return db_user
