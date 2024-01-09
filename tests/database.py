from collections.abc import AsyncGenerator

from sqlalchemy.engine import URL, create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm.session import sessionmaker

from api.config import settings
from api.database import Base

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

engine_test_async = create_async_engine(
    url=SQLALCHEMY_DATABASE_TEST_URL_async,
    pool_pre_ping=True,
)

TestingSession = sessionmaker(
    bind=engine_test_async,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)  # type: ignore


async def override_get_db() -> AsyncGenerator:
    async with TestingSession() as session:
        yield session


async def create_tables_async() -> None:
    async with engine_test_async.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_tables_async() -> None:
    async with engine_test_async.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


# SYNC
engine_test = create_engine(
    SQLALCHEMY_DATABASE_TEST_URL,
    pool_pre_ping=True,
)


def create_tables() -> None:
    Base.metadata.create_all(bind=engine_test)


def drop_tables() -> None:
    Base.metadata.drop_all(bind=engine_test)
