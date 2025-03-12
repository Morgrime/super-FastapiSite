from fastapi import APIRouter, Depends, HTTPException
from fastapi import Form
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import get_session
from app.database.crud import (create_user,
                           get_user_by_username,
                           create_user_profile)
from app.schemas.user_scheme import UserWithProfileResponse, UserProfileResponse
from app.utils.security import hash_password, verify_password, change_password
from app.utils.auth import create_access_token
from app.utils.dependencies import get_current_user
from datetime import timedelta


router = APIRouter()


@router.post("/register",
             response_model=UserWithProfileResponse,
             tags=["Authentication"])
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


@router.post("/change_password", tags=["User"])
async def change_password_route(
    old_password: str = Form(...),
    new_password: str = Form(...),
    current_user: dict = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    try:
        user = await change_password(session,
                                     current_user,
                                     old_password,
                                     new_password)
        return user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
