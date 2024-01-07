import uuid

from httpx import AsyncClient


async def test_stat_empty_request(async_client: AsyncClient) -> None:
    response = await async_client.get(
        "/api/stat",
    )
    assert response.status_code == 422


async def test_stat_404(async_client: AsyncClient) -> None:
    obj_id = uuid.uuid4()
    response = await async_client.get(
        f"/api/stat?query_id={obj_id}",
    )
    assert response.status_code == 404


async def test_add(async_client: AsyncClient) -> None:
    response = await async_client.post(
        "/api/add?region_id=1&category_id=1&query=asd",
    )
    assert response.status_code == 201


async def test_add_repeat(async_client: AsyncClient) -> None:
    _ = await async_client.post(
        "/api/add?region_id=2&category_id=3&query=asd",
    )
    response = await async_client.post(
        "/api/add?region_id=2&category_id=3&query=asd",
    )
    assert response.status_code == 409


async def test_add_stat(async_client: AsyncClient) -> None:
    response_query = await async_client.post(
        "/api/add?region_id=4&category_id=5&query=asd",
    )
    assert response_query.status_code == 201
    data = response_query.json()
    obj_id = data["query_id"]

    response_stat = await async_client.get(
        f"/api/stat?query_id={obj_id}",
    )
    assert response_stat.status_code == 200
