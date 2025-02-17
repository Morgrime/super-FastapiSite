from fastapi import APIRouter, Depends
from utils.dependencies import get_current_user


router = APIRouter()


@router.get("/protected-route", tags=["Protected"])
async def protected_route(current_user: dict = Depends(get_current_user)):
    return {"message": "This is a protected route", "user": current_user}


@router.get('/test', tags=["Protected"])
async def test_page(current_user: dict = Depends(get_current_user)):
    return 'Test page'
 