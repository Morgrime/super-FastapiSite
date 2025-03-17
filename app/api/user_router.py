from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from app.utils.dependencies import get_current_user
from app.database.session import get_session
from app.models.models import User
from app.schemas.user_scheme import (UserProfileResponse,
                                     UserWithProfileResponse)


router = APIRouter()


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
