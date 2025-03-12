from fastapi import FastAPI
from uvicorn import run
from contextlib import asynccontextmanager
from app.database.session import engine
from app.models.base import Base
from app.api import main_router as main_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # тут начало работы sql
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # тут остановочка
    await engine.dispose()

app = FastAPI(lifespan=lifespan, debug=True)
app.include_router(main_router)


if __name__ == "__main__":
    run(app)
