from collections.abc import AsyncGenerator

import pytest_asyncio
from httpx import AsyncClient

from main import app


@pytest_asyncio.fixture(scope="session")
async def async_client() -> AsyncGenerator:
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client
