from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import SessionLocal
from app.database.crud import create_user, get_user, update_user, delete_user
from app.schemas.user_scheme import UserCreate, UserUpdate

router = APIRouter()


async def get_session():
    async with SessionLocal() as session:
        yield session


@router.post("/users/", response_model=UserCreate)
async def create_user_route(user: UserCreate,
                            session: AsyncSession = Depends(get_session)):
    new_user = await create_user(session,
                                 user.username, 
                                 user.hashed_password,
                                 user.email)
    return new_user


@router.get("/users/{user_id}", response_model=UserCreate)
async def read_user_route(user_id: int,
                          session: AsyncSession = Depends(get_session)):
    user = await get_user(session, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/users/{user_id}", response_model=UserUpdate)
async def update_user_route(user_id: int,
                            user_update: UserUpdate,
                            session: AsyncSession = Depends(get_session)):
    user = await update_user(session,
                             user_id,
                             user_update.username,
                             user_update.hashed_password,
                             user_update.email)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.delete("/users/{user_id}", response_model=UserCreate)
async def delete_user_route(user_id: int,
                            session: AsyncSession = Depends(get_session)):
    user = await delete_user(session, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")