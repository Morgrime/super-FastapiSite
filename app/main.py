from fastapi import FastAPI
from uvicorn import run
from contextlib import asynccontextmanager
from routers.index_router import router as routing_router
from routers.crud_router import router as crud_router
from routers.auth_router import router as auth_router
from routers.user_router import router as user_router
from database.session import engine
from models.base import Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    # тут начало работы sql
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # тут остановочка
    await engine.dispose()

app = FastAPI(lifespan=lifespan)

app.include_router(routing_router)
app.include_router(crud_router)
app.include_router(auth_router)
app.include_router(user_router)


if __name__ == "__main__":
    run(app)
