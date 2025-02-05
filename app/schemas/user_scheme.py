from pydantic import BaseModel

class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    hashed_password: str

class UserUpdate(UserBase):
    hashed_password: str

class User(UserBase):
    id: int

    class Config:
        orm_mode = True