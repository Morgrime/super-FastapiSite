from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
import os


# создаёт дб в папке database
DATABASE_URL = f"sqlite+aiosqlite:///{os.path.join(os.getcwd(), 'app', 'database', 'database.db')}"


engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(
    autoflush=False,
    bind=engine,
    class_=AsyncSession
)


async def get_session():
    async with SessionLocal() as session:
        yield session
