from collections.abc import AsyncGenerator, Generator

import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy_utils.functions import (  # type: ignore
    create_database,
    database_exists,
    drop_database,
)

from api.database import get_db
from main import app

from .database import (
    SQLALCHEMY_DATABASE_TEST_URL,
    TestingSession,
    create_tables,
    drop_tables,
    engine_test_async,
    override_get_db,
)


@pytest_asyncio.fixture(scope="function")
async def async_client() -> AsyncGenerator:
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest.fixture(scope="session")
def _create_db() -> Generator:
    app.dependency_overrides[get_db] = override_get_db
    if not database_exists(SQLALCHEMY_DATABASE_TEST_URL):
        create_database(SQLALCHEMY_DATABASE_TEST_URL)
    yield
    drop_database(SQLALCHEMY_DATABASE_TEST_URL)


@pytest.fixture(scope="session")
def _create_tables(_create_db) -> Generator:  # noqa: ANN001, U101
    create_tables()
    yield
    drop_tables()


@pytest_asyncio.fixture(scope="function")
async def async_db_engine(_create_tables) -> AsyncGenerator:  # noqa: ANN001, U101
    yield engine_test_async


@pytest_asyncio.fixture(scope="function")
async def async_db(async_db_engine) -> AsyncGenerator:  # noqa: ANN001, U100
    async with TestingSession() as session:
        yield session
