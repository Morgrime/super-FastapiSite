from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database.session import SessionLocal
from database.crud import create_user, get_user_by_username
from schemas.user_scheme import UserCreate, UserLogin
from utils.security import hash_password, verify_password
from utils.auth import create_access_token
from datetime import timedelta


router = APIRouter()


async def get_session():
    async with SessionLocal() as session:
        yield session


@router.post("/register", response_model=UserCreate, tags=["Authentication"])
async def register_user(user: UserCreate,
                        session: AsyncSession = Depends(get_session)):
    existing_user = await get_user_by_username(session, user.username)
    if existing_user:
        raise HTTPException(status_code=400,
                            detail="Username already registered")

    hashed_password = hash_password(user.hashed_password)
    new_user = await create_user(session,
                                 user.username,
                                 hashed_password,
                                 user.email)
    return new_user


@router.post("/login", tags=["Authentication"])
async def login_user(user: UserLogin,
                     session: AsyncSession = Depends(get_session)):
    db_user = await get_user_by_username(session, user.username)
    if not db_user:
        raise HTTPException(status_code=400, detail="User does not exist")

    if not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect password")

    # JWT
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": db_user.username},
        expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}
