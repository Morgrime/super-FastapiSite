from fastapi import APIRouter
from app.api.index_router import router as routing_router
from app.api.crud_router import router as crud_router
from app.api.auth_router import router as auth_router
from app.api.user_router import router as user_router

main_router = APIRouter()

main_router.include_router(routing_router)
main_router.include_router(crud_router)
main_router.include_router(auth_router)
main_router.include_router(user_router)

__all__ = ["main_router"]