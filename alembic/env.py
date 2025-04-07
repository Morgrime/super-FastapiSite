from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import AsyncEngine

from alembic import context

from app.database.config import settings
from app.models.base import Base
from app.models.models import UserProfile, User

import asyncio

config = context.config
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL_aiosqlite)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def do_run_migrations(connection):
    """Выполняет миграции в синхронном контексте."""
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,  # Добавьте, если хотите сравнивать типы столбцов
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online():
    """Запускает миграции в асинхронном режиме."""
    connectable = AsyncEngine(
        engine_from_config(
            config.get_section(config.config_ini_section),
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,
            future=True,
        )
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)


def run_migrations_offline():
    """Запускает миграции в автономном режиме."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())