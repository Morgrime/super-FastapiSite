from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from utils.dependencies import get_current_user
from database.session import get_session
from database.crud import get_user_by_username
from models.models import User
from schemas.user_scheme import UserProfileResponse, UserWithProfileResponse


router = APIRouter()


# хуета какая-то если добавить response_model=UserResponse
# TODO решить проблему с валидацией
@router.get("/profile", response_model=UserWithProfileResponse, tags=["User"])
async def get_profile(current_user: dict = Depends(get_current_user),
                      session: AsyncSession = Depends(get_session)):
    result = await session.execute(
        select(User).options(selectinload(User.profile)).where(User.username == current_user["sub"])
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="Profile not found")

    # Преобразование данных для ответа
    profile_data = UserProfileResponse(
        full_name=user.profile.full_name if user.profile else None,
        bio=user.profile.bio if user.profile else None,
        created_at=user.profile.created_at if user.profile else None,
        updated_at=user.profile.updated_at if user.profile else None
    )

    response_data = UserWithProfileResponse(
        username=user.username,
        email=user.email,
        profile=profile_data
    )

    return response_data



# @router.get("/profile", tags=["User"])
# async def get_profile(current_user: dict = Depends(get_current_user),
#                       session: AsyncSession = Depends(get_session)):
#     user = await get_user_by_username(session, current_user["sub"])
#     if not user:
#         raise HTTPException(status_code=404, detail="Profiel not found")
#     return user