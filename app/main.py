from fastapi import FastAPI
from uvicorn import run
from contextlib import asynccontextmanager
from routers.index_router import router as routing_router
from routers.crud_router import router as crud_router
from app.database.session import engine, SessionLocal

@asynccontextmanager
async def lifespan(app: FastAPI):
    # тут начало работы sql
    async with engine.begin() as conn:
        await conn.run_sync(SessionLocal.metadata.create_all)
    yield
    # тут остановочка
    await engine.dispose()

app = FastAPI(lifespan=lifespan)

app.include_router(routing_router)
app.include_router(crud_router)



# if __name__ == "__main__":
#     run(app)