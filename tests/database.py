from collections.abc import AsyncGenerator

from sqlalchemy.engine import URL, create_engine
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from src.api.config import settings
from src.api.models import Base

SQLALCHEMY_DATABASE_TEST_URL = URL.create(
    drivername="postgresql",
    username=settings.POSTGRES_USER,
    password=settings.POSTGRES_PASSWORD,
    host=settings.POSTGRES_HOST,
    port=settings.POSTGRES_PORT,
    database=f"{settings.POSTGRES_DB}_test",
)

SQLALCHEMY_DATABASE_TEST_URL_async = URL.create(
    drivername="postgresql+asyncpg",
    username=settings.POSTGRES_USER,
    password=settings.POSTGRES_PASSWORD,
    host=settings.POSTGRES_HOST,
    port=settings.POSTGRES_PORT,
    database=f"{settings.POSTGRES_DB}_test",
)


async def override_get_db() -> AsyncGenerator:
    async_engine = create_async_engine(
        url=SQLALCHEMY_DATABASE_TEST_URL_async,
        pool_pre_ping=True,
    )
    _session = async_sessionmaker(
        bind=async_engine,
        expire_on_commit=False,
        autocommit=False,
        autoflush=False,
    )
    async with _session() as session:
        yield session

    await async_engine.dispose()


# SYNC
engine_test = create_engine(
    SQLALCHEMY_DATABASE_TEST_URL,
    pool_pre_ping=True,
)


def create_tables() -> None:
    Base.metadata.create_all(bind=engine_test)


def drop_tables() -> None:
    Base.metadata.drop_all(bind=engine_test)
