from fastapi import APIRouter, Depends, HTTPException
from fastapi import Form
from sqlalchemy.ext.asyncio import AsyncSession
from database.session import get_session
from database.crud import create_user, get_user_by_username, create_user_profile
from schemas.user_scheme import UserCreate, UserResponse, UserWithProfileResponse, UserProfileResponse
from utils.security import hash_password, verify_password
from utils.auth import create_access_token
from datetime import timedelta


router = APIRouter()


@router.post("/register", response_model=UserWithProfileResponse, tags=["Authentication"])
async def register_user(username: str = Form(),
                        email: str = Form(),
                        password: str = Form(),
                        session: AsyncSession = Depends(get_session)):
    existing_user = await get_user_by_username(session, username)
    if existing_user:
        raise HTTPException(status_code=400,
                            detail="Username already registered")

    hashed_password = hash_password(password)
    new_user = await create_user(session,
                                 username,
                                 hashed_password,
                                 email)
    new_profile = await create_user_profile(session, new_user.id)

    # Преобразование данных для ответа
    profile_data = UserProfileResponse(
        full_name=new_profile.full_name,
        bio=new_profile.bio,
        created_at=new_profile.created_at,
        updated_at=new_profile.updated_at
    )

    response_data = UserWithProfileResponse(
        username=new_user.username,
        email=new_user.email,
        profile=profile_data
    )

    return response_data


@router.post("/login", tags=["Authentication"])
async def login_user(username: str = Form(),
                     password: str = Form(),
                     session: AsyncSession = Depends(get_session)):
    db_user = await get_user_by_username(session, username)
    if not db_user:
        raise HTTPException(status_code=400, detail="User does not exist")

    if not verify_password(password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect password")

    # JWT
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": db_user.username},
        expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}
