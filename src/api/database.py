import logging
from collections.abc import AsyncGenerator

from sqlalchemy import select, text
from sqlalchemy.engine import URL, create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from src.api.config import settings
from src.api.models.base import Base

SQLALCHEMY_DATABASE_URL = URL.create(
    drivername="postgresql",
    username=settings.POSTGRES_USER,
    password=settings.POSTGRES_PASSWORD,
    host=settings.POSTGRES_HOST,
    port=settings.POSTGRES_PORT,
    database=settings.POSTGRES_DB,
)

SQLALCHEMY_DATABASE_URL_async = URL.create(
    drivername="postgresql+asyncpg",
    username=settings.POSTGRES_USER,
    password=settings.POSTGRES_PASSWORD,
    host=settings.POSTGRES_HOST,
    port=settings.POSTGRES_PORT,
    database=settings.POSTGRES_DB,
)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,
    echo=settings.db_echo_log,
)

engine_async = create_async_engine(
    SQLALCHEMY_DATABASE_URL_async,
    pool_pre_ping=True,
    echo=settings.db_echo_log,
    future=True,
)


async_session = sessionmaker(bind=engine_async, class_=AsyncSession, expire_on_commit=False)  # type: ignore


async def ping_db(session: AsyncSession) -> bool:
    try:
        await session.execute(select(text("1")))
    except Exception:
        logging.error(f"Error ping db {'DBNAME'}")
        return False

    return True


async def get_db() -> AsyncGenerator:
    async with async_session() as session:
        yield session


# async def async_create_tables() -> None:
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)
#
#
# async def async_drop_tables() -> None:
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.drop_all)


def create_tables() -> None:
    Base.metadata.create_all(bind=engine)


def drop_tables() -> None:
    Base.metadata.drop_all(bind=engine)
