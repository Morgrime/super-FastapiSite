from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from utils.dependencies import get_current_user
from database.session import get_session
from database.crud import get_user_by_username
from schemas.user_scheme import UserResponse


router = APIRouter()


@router.get("/profile", response_model=UserResponse, tags=["User"])
async def get_profile(current_user: dict = Depends(get_current_user),
                      session: AsyncSession = Depends(get_session)):
    user = await get_user_by_username(session, current_user["sub"])
    if not user:
        raise HTTPException(status_code=404, detail="Profiel not found")
    return user


