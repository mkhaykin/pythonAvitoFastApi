from collections.abc import AsyncGenerator, Generator

import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy import DDL
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy_utils.functions import (  # type: ignore
    create_database,
    database_exists,
    drop_database,
)

from api.database import get_db
from main import app

from .database import (
    SQLALCHEMY_DATABASE_TEST_URL,
    SQLALCHEMY_DATABASE_TEST_URL_async,
    create_tables,
    drop_tables,
    override_get_db,
)


@pytest_asyncio.fixture(scope="function")
async def async_client() -> AsyncGenerator:
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest.fixture(scope="session", autouse=True)
def _create_db() -> Generator:
    app.dependency_overrides[get_db] = override_get_db
    if not database_exists(SQLALCHEMY_DATABASE_TEST_URL):
        create_database(SQLALCHEMY_DATABASE_TEST_URL)
    yield
    drop_database(SQLALCHEMY_DATABASE_TEST_URL)


@pytest.fixture(scope="module", autouse=True)
def _create_tables(_create_db) -> Generator:  # noqa: ANN001, U101
    create_tables()
    yield
    drop_tables()


@pytest_asyncio.fixture()
async def async_engine() -> AsyncGenerator:
    engine = create_async_engine(
        url=SQLALCHEMY_DATABASE_TEST_URL_async,
        pool_pre_ping=True,
    )
    yield engine
    await engine.dispose()


@pytest_asyncio.fixture()
async def async_session(
    async_engine: AsyncEngine,
) -> AsyncGenerator[AsyncSession, None]:
    _session = async_sessionmaker(
        bind=async_engine,
        expire_on_commit=False,
        autocommit=False,
        autoflush=False,
    )
    async with _session() as session:
        yield session


@pytest_asyncio.fixture()
async def clear_tables(
    async_session: AsyncSession,
) -> None:
    stmt = DDL(
        """
    DO $$ DECLARE
        r RECORD;
    BEGIN
        FOR r IN (SELECT tablename FROM pg_tables WHERE schemaname = current_schema()) LOOP
            EXECUTE 'TRUNCATE TABLE ' || quote_ident(r.tablename) || ' CASCADE';
        END LOOP;
    END $$;
    """,
    )
    await async_session.execute(stmt)
    return
