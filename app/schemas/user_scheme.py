from pydantic import BaseModel, EmailStr


# база для внесения в бд
class UserBase(BaseModel):
    username: str
    email: EmailStr


# создание пользователя /crud.py create_user
class UserCreate(UserBase):
    hashed_password: str | int


# обновление данных пользователя /crud.py update_user
class UserUpdate(UserBase):
    hashed_password: str | int


# удаление пользователя по id /crud.py delete_user
class UserDelete(BaseModel):
    detail: str


# вход в аккаунт /auth_router.py login_user
class UserLogin(BaseModel):
    username: str
    password: str


# модель для ответа на запросы по
# получению всех пользователей /crud_router.py get_users
class User(UserBase):
    id: int

    class Config:
        orm_mode = True
