from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"])


# хэш пароля
def hash_password(password: str) -> str:
    return pwd_context.hash(password)


# проверка пароля
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
