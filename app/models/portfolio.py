from sqlalchemy import String, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base import Base
from datetime import datetime


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String, unique=True, index=True)
    hashed_password: Mapped[str]
    email: Mapped[str] = mapped_column(String, unique=True, index=True)

    """связь по двух таблиц чтобы при удалении
      профиля, удалялась и инфа о пользователе"""
    profile: Mapped["UserProfile"] = relationship("UserProfile",
                                                  back_populates="user",
                                                  uselist=False,
                                                  cascade="all, delete-orphan")


class UserProfile(Base):
    __tablename__ = 'user_profiles'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"),
                                         unique=True,
                                         nullable=True)
    full_name: Mapped[str] = mapped_column(index=True, nullable=True)
    bio: Mapped[str] = mapped_column(nullable=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime,
                                                 default=datetime.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime,
                                                 default=datetime.now(),
                                                 onupdate=datetime.now())

    user: Mapped["User"] = relationship("User", back_populates="profile")