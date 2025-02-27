from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from models.models import User

pwd_context = CryptContext(schemes=["bcrypt"])


# тут происходит хэширование пароля
def hash_password(password: str) -> str:
    return pwd_context.hash(password)


# тут происходит проверка правильности ввода пароля
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# тут происходит смена пароля
async def change_password(session: AsyncSession,
                          user: User,
                          old_password: str,
                          new_password: str) -> bool:
    if not verify_password(old_password, user.hashed_password):
        raise ValueError("Invalid old password")

    user.hashed_password = hash_password(new_password)
    await session.commit()
    await session.refresh(user)
    return user
