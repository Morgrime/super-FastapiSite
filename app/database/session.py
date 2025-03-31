from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.database.config import settings


engine = create_async_engine(settings.DATABASE_URL_aiosqlite, echo=True)
SessionLocal = sessionmaker(
    autoflush=False,
    bind=engine,
    class_=AsyncSession
)


async def get_session():
    async with SessionLocal() as session:
        yield session
