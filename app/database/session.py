from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os


load_dotenv()

# создаёт дб в папке database
# DATABASE_URL = f"sqlite+aiosqlite:///{os.path.join(os.getcwd(),
# 'app',
# 'database',
# 'database.db')}"
# создаёт дб в папке с файлом main (если запуск был из той же директории)
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(
    autoflush=False,
    bind=engine,
    class_=AsyncSession
)


async def get_session():
    async with SessionLocal() as session:
        yield session
