from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = f"sqlite+aiosqlite:///{os.path.join(os.getcwd(), 'database.db')}"

engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(
    autoflush=False, bind=engine, class_=AsyncSession
)