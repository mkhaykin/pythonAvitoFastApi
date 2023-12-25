from httpx import AsyncClient


async def test_hello(async_client: AsyncClient):
    response = await async_client.get('/')
    assert response.status_code == 200
    assert response.json() == {'msg': 'Hello World'}


async def test_echo(async_client: AsyncClient):
    response = await async_client.get('/echo/message')
    assert response.status_code == 200
    assert response.json() == {'msg': 'message'}
