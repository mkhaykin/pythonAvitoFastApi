import pytest_asyncio
from main import app
from httpx import AsyncClient

# DEPRECATED (see __init__.py)
# @pytest.fixture(scope="session")
# def event_loop():
#
#     """Create an instance of the default event loop for each test case."""
#     loop = asyncio.get_event_loop()
#     yield loop
#     loop.close()


@pytest_asyncio.fixture(scope='module')
async def async_client() -> AsyncClient:
    async with AsyncClient(app=app, base_url='http://test') as client:
        yield client
